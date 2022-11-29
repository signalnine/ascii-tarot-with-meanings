#!/usr/bin/env node

//const inquirer = require('inquirer');
const cards = require('./cards');
//const CliFrames = require('cli-frames');
const os = require('os');
const yargs = require('yargs');
const reverseOdds = 5; //odds of a reverse between 0 and 100


const argv = yargs
  .option('random', {
    alias: 'r',
    description: 'Use random instead of user/date',
    type: 'boolean',
    default: false
  })
  .option('reverse_odds', {
    alias: 'o',
    description: 'Odds of a reversed card',
    type: 'number'
  })
  .help()
  .alias('help', 'h').argv;

if (argv.reverse_odds){
    if (argv.reverse_odds < 0){
        reverseOdds = 0
    } else if (argv.reverse_odds >= 100){
        reverseOdds = 100
    } else {
        reverseOdds = argv.reverse_odd
    };
}

//const asciiloader = [ '*', '*:', '*:･', '*:･ﾟ', '*:･ﾟ✧', '*:･ﾟ✧*', '*:･ﾟ✧*:', '*:･ﾟ✧*:･', '*:･ﾟ✧*:･ﾟ', '*:･ﾟ✧*:･ﾟ✧' ];




/**
 * Returns a hash code from a string
 * @param  {String} str The string to hash.
 * @return {Number}    A 32bit integer
 * @see http://werxltd.com/wp/2010/05/13/javascript-implementation-of-javas-string-hashcode-method/
 */
function hashCode(str) {
    let hash = 0;
    for (let i = 0, len = str.length; i < len; i++) {
        let chr = str.charCodeAt(i);
        hash = (hash << 5) - hash + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
}

const {deck}  = cards;

var salt = "butdtqqffs22";
var reverseStr = '';
var isReversed = false;
var hashval = today + user + salt;
var rawHash = hashCode(hashval);
var today = (new Date()).toString().split(' ').splice(1,3).join(' ');
var user = `${os.userInfo().username}`;
var t = 0;
if (argv.random){
    rawHash = Math.abs(Math.floor(Math.random() * 1000000));
}

t = Math.abs(rawHash) % deck.length;

console.log(`t = ${t}`);

if (reverseOdds > 0 && reverseOdds < 100){
    var reverseChk = Math.abs(rawHash) % 100;
    isReversed = (reverseChk <= reverseOdds) ? true : false;
    reverseStr = (isReversed) ? "reversed" : "";
} else if (reverseOdds >= 100) {
    isReversed = true;
    reverseStr = "reversed";
} else {
    isReversed = true;
}


//const loader = new CliFrames();
//loader.load(asciiloader);

console.log(`【☆】★【☆】★【☆】★【☆】★【☆】★【☆】★【☆】★【☆】★【☆】 \n`);
//console.log(`hashval = ${t}`);
console.log(`Today's tarot draw for ${user} is ....`);
console.log(`\n     【☆】${reverseStr} ${deck[t].name}【☆】`);
if (isReversed) {console.log(`${deck[t].reversed}`)} else { console.log(`${deck[t].card}\n`)};
if (isReversed) {console.log(`Meaning: ${deck[t].rdesc}`)} else {console.log(`Meaning: ${deck[t].desc}\n`)};
if (deck[t].cbd_desc != '') {console.log(`Description: ${deck[t].cbd_desc}\n`)};
console.log(`【☆】★【☆】★【☆】★【☆】★【☆】★【☆】★【☆】★【☆】★【☆】`);

/*

const pickspread = [
    {
        type: 'list',
        name: 'spread',
        message: 'Select your spread',
        choices: ['One card', 'Three cards', 'Celtic cross', 'Show me the deck'],
        filter: function(val) {
            return val;
        }
    }
]

const exit = [
    {
        type: 'confirm',
        name: 'exit',
        message: 'Finished?',
        default: true
    }
]

function displayCard(x) {
    console.log(deck[x].name);
    console.log(deck[x].card);
}

function pickCard(message) {
    setTimeout(function() {
        console.log(message);
        setTimeout(function() {
            const chosenCard = Math.floor(Math.random() * deck.length);
            displayCard(chosenCard);
        }, 1000);
    }, 1000);
}

function end() {
    inquirer.prompt(exit).then(answer => {
        if (answer.exit) {
            loader.start();
            setTimeout(function() {
                console.log('Goodbye');
            }, 1000);
            return;
        } else { 
            run(); 
        }
    });
}

function displaySpread(type) {
    console.log(type);
    switch (type) {
        case 'One card':
            loader.start();
            pickCard('Your card is:');
            setTimeout(() => {
                end();
            }, 5000);
            return;
        case 'Three cards':
            loader.start();
            pickCard('Past:');
            setTimeout(function(){
                loader.start();
                pickCard('Present:');
            }, 3000);
            setTimeout(function(){
                loader.start();
                pickCard('Future:');
            }, 6000);
            setTimeout(() => {
                end();
            }, 11000);
            return;
        case 'Celtic cross':
            loader.start();
            pickCard('Yourself:');
            setTimeout(function(){
                loader.start();
                pickCard('Your obstacle:');
            }, 4000);
            setTimeout(function(){
                loader.start();
                pickCard('Root of the question:');
            }, 8000);
            setTimeout(function(){
                loader.start();
                pickCard('The past:');
            }, 12000);
            setTimeout(function(){
                loader.start();
                pickCard('Hopes/fears:');
            }, 16000);
            setTimeout(function(){
                loader.start();
                pickCard('The future:');
            }, 20000);
            setTimeout(function(){
                loader.start();
                pickCard('The root of the outcome:');
            }, 24000);
            setTimeout(function(){
                loader.start();
                pickCard('Others in the outcome:');
            }, 28000);
            setTimeout(function(){
                loader.start();
                pickCard('Hopes/fears for outcome:');
            }, 32000);
            setTimeout(function(){
                loader.start();
                pickCard('Outcome:');
            }, 36000);
            setTimeout(() => {
                end();
            }, 41000);
            return;
        case 'Show me the deck':
            for (let i = 0; i < 78; i++) {
                (function (i) {
                    setTimeout(function() {
                        displayCard(i);
                    }, 2000*i);
                })(i);
            };
            setTimeout(() => {
                end();
            }, 159000);
            return;
    }
}

function run() {
    inquirer.prompt(pickspread).then(answer => {
        const type = answer.spread;
        displaySpread(type);
    });
}

run(); */