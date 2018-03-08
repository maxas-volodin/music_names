

var plan = ["############################",
            "#      #    #      o      ##",
            "#                          #",
            "#   ~      #####           #",
            "##         #   #    ##     #",
            "###           ##     #     #",
            "#           ###      #     #",
            "#   ####                   #",
            "#   ##       o             #",
            "# o  #         o       ### #",
            "#    #                     #",
            "############################"];

// var plan = ["############################",
//             "#      #    #             ##",
//             "#                          #",
//             "#          #####           #",
//             "##         #   #    ##     #",
//             "###           ##     #     #",
//             "#           ###      #     #",
//             "#   ####                   #",
//             "#   ##                     #",
//             "# o  #                 ### #",
//             "#    #                     #",
//             "############################"];

var directions = "n ne e se s sw w nw";

function Point (x, y)
{
    this.x = x;
    this.y = y;
}

Point.prototype.isBlank = function () {return this.x == 0 && this.y == 0;}

Point.prototype.move = function (moveDir)
{
    switch (moveDir)
    {
        case "n": this.y --; break;
        case "ne": this.y --; this.x ++; break;
        case "e": this.x ++; break;
        case "se": this.x ++; this.y ++; break;
        case "s": this.y ++; break;
        case "sw": this.y ++; this.x --; break;
        case "w": this.x --; break;
        case "nw": this.x --; this.y --; break;
        default: console.log ("Wrong moveDir: ", moveDir);
    }
}

function Creature (location)
{
    this.location = location;
    this.visible = true;

    this.direction = "e";
}

Creature.prototype.findDirection = function (grid)
{
    if (grid != undefined)
    {
        var availDirs = [];
        var dirNames = directions.split (" ");

        dirNames.forEach (function (value) {
            var testPoint = new Point (this.location.x, this.location.y);
            testPoint.move (value);
            if (grid.contains (testPoint) && grid.vacant (testPoint)) availDirs.push (value);}, this
        );

        if (availDirs.length)
            this.direction = availDirs [Math.floor (Math.random () * availDirs.length)];

        return true;
    }
    else return false;
}

Creature.prototype.act = function (grid)
{
    // erase creature's mark off the map

    this.visible = false;
    grid.visualizeCreature (this);

    var newPoint = new Point (this.location.x, this.location.y);
    newPoint.move (this.direction);

    if (grid.contains (newPoint) == false || grid.vacant (newPoint) == false)
    {
        if (this.findDirection (grid) == false) newPoint = this.location;
        else {newPoint = this.location; newPoint.move (this.direction);}
    }

    this.location = newPoint;

    // visualize the creature once again

    this.visible = true;
    grid.visualizeCreature (this);
}

Creature.prototype.getAppearance = function ()
{
    return this.visible? "o" : " ";
}

// Critter section

function Critter (location)
{
    Creature.call (this, location);

    this.direction = "n";
    this.wallFound = false;
}

Critter.prototype = Object.create (Creature.prototype);
Critter.prototype.constructor = Critter;

Critter.prototype.getAppearance = function ()
{
    return this.visible? "~" : " ";
}

Critter.prototype.dirRight = function ()
{
    switch (this.direction)
    {
        case "n": return "e";
        case "w": return "n";
        case "s": return "w";
        case "e": return "s";
        default: console.log ("Wrong direction in turnLeft: ", this.direction); return "n";
    }
}

Critter.prototype.dirLeft = function ()
{
    switch (this.direction)
    {
        case "n": return "w";
        case "w": return "s";
        case "s": return "e";
        case "e": return "n";
        default: console.log ("Wrong direction in turnRight: ", this.direction); return "n";
    }
}

Critter.prototype.thereIsWallOnTheLeft = function (grid, newLocation)
{
    var charAtTarget;
    var newPlace = new Point (newLocation.x, newLocation.y);

    newPlace.move (this.dirLeft ());
    charAtTarget = grid.getCharAt (newPlace);

    return charAtTarget == "#";
}

Critter.prototype.act = function (grid)
{
    // erase creature's mark off the map

    this.visible = false;
    grid.visualizeCreature (this);

    var newPoint = new Point (this.location.x, this.location.y);

    if (this.wallFound && this.thereIsWallOnTheLeft (grid, this.location) == false)
    {
        this.direction = this.dirLeft ();
        newPoint.move (this.direction);
    }
    else
    {
        newPoint.move (this.direction);
        
        if (grid.contains (newPoint) == false || grid.vacant (newPoint) == false)
        {
            if (this.findDirection (grid) == false) newPoint = this.location;
            else {newPoint = this.location; newPoint.move (this.direction);}
        }
    }

    this.location = newPoint;

    // visualize the creature once again

    this.visible = true;
    grid.visualizeCreature (this);
}

Critter.prototype.findDirection = function (grid)
{
    if (grid != undefined)
    {
        for (;;)
        {
            var newLoc = new Point (this.location.x, this.location.y);
            newLoc.move (this.direction);

            switch (grid.getCharAt (newLoc))
            {
                case "o":
                case "~":
                    return false;   // do not move in case we bump into another creature
                case "#":           // if we move into a wall then turn right and look again
                    this.direction = this.dirRight (); this.wallFound = true; break;
                case " ":           // if the space is empty then all good, we can move
                    return true;
                default: console.log ("Unexpected char ", this.direction, " in Critter.findDirection"); return false;
            }
        }
    }
}

// Grid section

function Grid (pattern)
{
    this.space = pattern;
    this.width = pattern [0].length;
    this.height = pattern.length;

    this.space = new Array ();

    pattern.forEach (function (value, index, array) {

        var i;

        for (i = 0; i < value.length; i ++)
            {this.space.push (value [i]);}
    }, this);

    // console.log (this.space.toString ());
}

Grid.prototype.contains = function (location)
{
    return (location.x >= 0 && location.y >= 0 && (location.x + location.y * this.width) < this.space.length);
}

Grid.prototype.getCharAt = function (location)
{
    console.assert (this.contains (location));

    var index = location.x + location.y * this.width;
    return this.space [index];
}

Grid.prototype.vacant = function (location)
{
    return this.getCharAt (location) == " ";
}

Grid.prototype.nextCreatureLocation = function (location)
{
    if (this.contains (location))
    {
        var index;

        console.log ("Width == ", this.width, ", height == ", this.height, "space.length == ", this.space.length);

        for (index = 1 + location.x + location.y * this.width; index < this.space.length; index ++)
        {
            // if (this.space [index] == "o") {console.log ("Index == ", index); return new Point (index % this.width, index / this.width);}
            if (this.space [index] == "o" || this.space [index] == "~") return new Point (index % this.width, Math.floor (index / this.width));
        }
    }
    else console.log ("Wrong X/Y in looking for next creature: " + location.x + ", " + location.y);

    return new Point (0, 0);
}

Grid.prototype.visualizeCreature = function (creature)
{
    var mark = creature.getAppearance ();
    var index = creature.location.x + creature.location.y * this.width;

    if (index < this.space.length)
    {
        this.space [index] = mark;
        // console.log (targetString, creature.location.x);
    }
    else console.log ("Cannot visualize creature at X/Y: ", creature.location.x, ", ", creature.location.y);
}

Grid.prototype.toString = function ()
{
    var output = "";

    this.space.forEach (function (el, index, array) {
        if (index && index % this.width == 0) output += "\n";
        output += el;
    }, this);

    return output;
}

// World is a grid and a set of creatures

function World (gridImage)
{
    var loc = new Point (0, 0);
    this.grid = new Grid (gridImage);
    this.creatures = new Array (0);

    // for safety's sake let's assume there can be no more than 50 creatures

    // while (false)
    while (this.creatures.length < 50)
    {
        loc = this.grid.nextCreatureLocation (loc);
        if (loc.isBlank ()) break;

        switch (this.grid.getCharAt (loc))
        {
            case "o": this.creatures.push (new Creature (loc)); break;
            case "~": this.creatures.push (new Critter (loc)); break;
            default: console.log ("Unexpected char " + this.grid.getCharAt (loc) + " at " + loc.x, ", ", loc.y); break;
        }
    }

    console.log ("World created, number of creatures == ", this.creatures.length);
}

World.prototype.turn = function ()
{
    this.creatures.forEach (function (el, index, ar) {el.act (this.grid)}, this);
    // this.creatures.forEach (function (el, index, ar) {console.log (this);}, this);
    this.creatures.forEach (function (el, index, ar) {this.grid.visualizeCreature (el)}, this);
}

World.prototype.toString = function ()
{
    // return "No world";
    return this.grid.toString ();
}

// var newWorld = new World (plan);
// console.log (newWorld.toString ());

// newWorld.turn ();
// console.log (newWorld.toString ());

animateWorld (new World (plan));
