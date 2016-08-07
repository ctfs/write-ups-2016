/**
 * flag -> ABCTF{node_is_w4Ck}
 *
 */

process.stdin.resume();
process.stdin.setEncoding('utf8');
console.log("Give me a flag");
process.stdin.on('data', (t) => {
    t = t.trim();
    if (t.length === 19) {
        if (t.substr(0, 5) === 'ABCTF') {
            if (t[5].charCodeAt(0) === t[18].charCodeAt(0) - 1 - 1 && t[5].charCodeAt(0) === 123) { /////// t[5] === '{' && t[18] === '}'
                if (t.substr(6, 4) === Object.keys(process.versions)[1]) { ///// t.substr(6, 4) === 'node'
                    if (t[10] === t[13] && t[10].charCodeAt(0) === 95) { ////// t[10] = t[13] = '_'
                        if (t.substr(11, 2) === (('undefined')[5] + ('string')[0])) { ///// t.substr(11, 2) === 'is'
                            if (t.substr(14, 4) === (32).toString(33) + 4 + 'C' + 'k') { ///t.substr(14, 4) === 'w4Ck'
                                console.log("nice job!");
                                process.exit();
                            }
                        }
                    }
                }
            }
        }
    }
    console.log("nope!");
    process.exit();
});
