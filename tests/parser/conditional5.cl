(* A conditional has the form if <expr> then <expr> else <expr> fi *)

class Main {
    main(): Object {
        (new Alpha).print()
    };
};

class Test {
    test1: Object;
    
    testing1(): Int {
        2 + 2
    };

    test2: Int <- 1;

    test3: String <- "1";

    testing2(a: Alpha, b: Int): Int {
        2 + 2
    };

    testing3(): String {
        "2 + 2"
    };

    testing4(x: Int, y: Int): Test {
        self
    };

    testing5(a: String, b: String): IO {
        If a.length() < b.length() THeN
            new IO.out_string("La cadena \"".concat(b).concat("\" es mas larga que la cadena \"").concat(a).concat("\"."))
        eLSe
            if a.length() = b.length() THeN
                new IO.out_string("La cadena \"".concat(a).concat("\" mide igual que la cadena \"").concat(b).concat("\"."))
            ElsE
                new IO.out_string("La cadena \"".concat(a).concat("\" es mas larga que la cadena \"").concat(b).concat("\"."))
            fI
        Fi
    };

    testing6(): Int {
        if true then true++ else 0 -- If branch must be an expression
    };
};

class Test2 {
    test1: Test <- new Test;

    testing1(): Test {
        test1.testing4(1 + 1, 1 + 2).testing4(2 + 3, 3 + 5).testing4(5 + 8, 8 + 13)
    };

    testing2(x: Int, y: Int): Test2 {
        self
    };

    testing3(): Test2 {
        testing2(1 + 1, 1 + 2).testing2(2 + 3, 3 + 5).testing2(5 + 8, true + fALSE)
    };

    testing4(): Object {
        test1@Object.copy()
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
