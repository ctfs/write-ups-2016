package main

import (
    "crypto/aes"
    "encoding/binary"
    "fmt"
    "io"
    "io/ioutil"
    "math/rand"
    "net"
    "strings"
    "strconv"
)

// How many trials to require
var THRESHOLD = 1000

func check(e error) {
    if e != nil {
        panic(e)
    }
}

type UserError struct {
    msg string // description of error
}
func (e *UserError) Error() string { return e.msg }

type Edge struct {
    vertex_1 uint32
    vertex_2 uint32
}

var vertices uint32
var edges []Edge

func load_graph() {
    contents, err := ioutil.ReadFile("graph.txt")
    check(err)
    lines := strings.Split(string(contents), "\n")
    for _, line := range lines {
        if len(line) == 0 {
            continue
        }
        if line[0] == '#' {
            words := strings.Split(line, " ")
            if len(words) != 2 {
                panic(UserError{"Bad vertex count line!"})
            }
            v, err := strconv.Atoi(words[1])
            check(err)
            vertices = uint32(v)
            continue
        }
        words := strings.Split(line, " ")
        if len(words) != 2 {
            panic(UserError{"Bad edge format!"})
        }
        v1, err := strconv.Atoi(words[0])
        check(err)
        v2, err := strconv.Atoi(words[1])
        check(err)
        edges = append(edges, Edge{uint32(v1), uint32(v2)})
    }
}

var flag string;

func load_flag() {
    f, err := ioutil.ReadFile("flag.txt")
    check(err)
    flag = strings.TrimRight(string(f), "\n")
}

func get_colors(conn net.Conn) [][]byte {
    result := make([][]byte, vertices)
    var i uint32
    for i = 0; i < vertices; i++ {
        cipher := make([]byte, 16)
        _, err := io.ReadFull(conn, cipher)
        check(err)
        result[i] = cipher
    }
    return result
}

func gen_challenge() (uint32, uint32) {
    edge := edges[rand.Intn(len(edges))]
    return edge.vertex_1, edge.vertex_2
}

func send_challenge(conn net.Conn, edge Edge) {
    buf := make([]byte, 4)
    binary.BigEndian.PutUint32(buf, edge.vertex_1)
    conn.Write(buf)
    binary.BigEndian.PutUint32(buf, edge.vertex_2)
    conn.Write(buf)
}

func get_keys(conn net.Conn) ([]byte, []byte) {
    key1 := make([]byte,16)
    key2 := make([]byte,16)
    _, err := io.ReadFull(conn, key1)
    check(err)
    _, err = io.ReadFull(conn, key2)
    check(err)
    return key1, key2
}

func decrypt(cipher []byte, key []byte) uint32 {
    c, err := aes.NewCipher(key)
    check(err)
    plain := make([]byte, 16)
    c.Decrypt(plain, cipher)
    var color uint32
    for ix, b := range plain {
        if ix == 0 {
            color = uint32(b)
            if color < 1 || color > 3 {
                panic(UserError{"Bad color: " + string(b)})
            }
        } else {
            if b != 0 {
                panic(UserError{"This isn't MITM III!"})
            }
        }
    }
    return color
}

func handle_connection(conn net.Conn) {
    defer func() {
        e := recover()
        if e != nil {
            if uerr, ok := e.(UserError); ok {
                conn.Write([]byte(uerr.Error()))
            }
        }
        conn.Close()
    }()

    successes := 0
    for {
        // Get the colors
        ciphers := get_colors(conn)
        // Send a challenge (pair of vertices)
        v1, v2 := gen_challenge()
        send_challenge(conn, Edge{v1, v2})
        // Get the AES keys
        k1, k2 := get_keys(conn)
        if decrypt(ciphers[v1], k1) == decrypt(ciphers[v2], k2) {
            // Colors don't match!
            panic(UserError{"Those are the same color!"})
            return;
        }
        successes += 1
        if successes == THRESHOLD {
            // Okay, I believe you
            conn.Write([]byte("BKPCTF{" + flag + "}"));
            conn.Close()
            return
        }
    }
}

func accept_connections() {
    listener, err := net.Listen("tcp", ":8001")
    check(err)
    defer listener.Close()
    for {
        conn, err := listener.Accept()
        check(err)
        go handle_connection(conn)
    }
}

func main() {
    load_graph()
    load_flag()
    fmt.Println("Ready to rumble.")
    accept_connections()
}
