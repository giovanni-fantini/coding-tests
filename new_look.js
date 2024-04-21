//jshint esnext:true

/**
 * Asserts "expected" versus "actual", 
 * 'failing' the assertion (via Error) if a difference is found.
 *
 * @param {String} message The comparison message passed by the user
 * @param {*} expected The expected item
 * @param {*} actual The actual item
 */
function assertEquals(message, expected, actual) {    
  //TODO: Time boxed to 30 minutes
// var testSuccess = False
// set flow conditions according to input types
// if { type of actual is string or integer }:
 //   if ( expected == actual ):
//       testSuccess = True
// elsif { type of actual is a collection }:
// prop_comparisons = {}
//    for prop in collection:
//       if prop == expected[prop.key]
//          prop_comparisons[prop.key] = True
//   testSuccess = prop_comparisons.unique == True
}


/* -- Test running code:  --- */

/**
* Runs a "assertEquals" test.
* 
* @param {String} message The initial message to pass
* @param {*} expected Expected item
* @param {*} actual The actual item
*/
function runTest({ message, expected, actual }) {
try {
  assertEquals(message, expected, actual);
} catch (error) {
  return error.message;
}
}

function runAll() {
var complexObject1 = {
  propA: 1,
  propB: {
    propA: [1, { propA: 'a', propB: 'b' }, 3],
    propB: 1,
    propC: 2
  }
};
var complexObject1Copy = {
  propA: 1,
  propB: {
    propA: [1, { propA: 'a', propB: 'b' }, 3],
    propB: 1,
    propC: 2
  }
};
var complexObject2 = {
  propA: 1,
  propB: {
    propB: 1,
    propA: [1, { propA: 'a', propB: 'c' }, 3],
    propC: 2
  }
};
var complexObject3 = {
  propA: 1,
  propB: {
    propA: [1, { propA: 'a', propB: 'b' }, 3],
    propB: 1
  }
};

var testCases = [
  { message: 'Test 01', expected: 'abc', actual: 'abc' },
  { message: 'Test 02', expected: 'abcdef', actual: 'abc' },
  { message: 'Test 03', expected: ['a'], actual: {0: 'a'} },
  { message: 'Test 04', expected: ['a', 'b'], actual: ['a', 'b', 'c'] },
  { message: 'Test 05', expected: ['a', 'b', 'c'], actual: ['a', 'b', 'c'] },
  { message: 'Test 06', expected: complexObject1, actual: complexObject1Copy },
  { message: 'Test 07', expected: complexObject1, actual: complexObject2 },
  { message: 'Test 08', expected: complexObject1, actual: complexObject3 },
  { message: 'Test 09', expected: null, actual: {} },
];

assertionFailures = testCases.map(runTest)
  .filter(result => result !== undefined)
  .forEach(addToList)
}

function addToList(message) {
var messagesEl = document.getElementById('messages');
var newListEl = document.createElement('li');
newListEl.innerHTML = message;
messagesEl.appendChild(newListEl);    
}

runAll();