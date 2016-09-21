import std.stdio;
import std.range;
import std.algorithm;
import std.string;
import std.traits;
import std.conv;

template enc(string key) {
    string enc(string s) pure @safe {
        pragma(msg, "encrypting with key...", key);
        char enc_add = cast(char) (s.length.to!int);
        string output = "";
        foreach(a,b; cycle(key).zip(s)) {
            output ~= a ^ b ^ enc_add;
        }
        return output;
    }
}

mixin template ForeachUnrolled(string F, int N, int MIN=1) {
    pragma(msg, "ForEach...", N, " to ", MIN);
    static if (N > 1) {
        mixin ForeachUnrolled!(F, N-1, MIN); 
    }
    mixin MakeFunction!(F, N);
}
mixin template MakeFunction(string F, alias T) {
    // Convert $ and %
    mixin(translate(F, ['$' : T.to!(string), '%' : (T-1).to!string]));
}

string encrypt(string s) pure @safe {
    const int n = 499; // 500 is DMD's template recursion limit
    //const int n = 30;
    string output_0 = s; // base case with our string
    mixin ForeachUnrolled!("string output_$ = enc!($$$.to!string)(output_%);", n);
    mixin("return output_" ~ n.to!string ~ ";");
}

string hexencode(string s) {
    string encoded = "";
    foreach (c; s) {
        encoded ~= format("%02x", c);
    }
    return encoded;
}

string enc_flag = encrypt("flag{t3mplat3_met4pr0gramming_is_gr8_4_3very0n3}");
void main() {
    writeln("Your hexencoded, encrypted flag is: ", enc_flag.hexencode);
    writeln("I generated it at compile time. :)");
    writeln("Can you decrypt it for me?");
}
