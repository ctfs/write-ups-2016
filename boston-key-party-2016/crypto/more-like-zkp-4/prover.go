package main

import (
    "crypto/aes"
    "crypto/cipher"
    crand "crypto/rand"
    "encoding/binary"
    "fmt"
    "io"
    "io/ioutil"
    "net"
    mrand "math/rand"
    "strings"
    "strconv"
)

type UserError struct {
    msg string // description of error
}
func (e *UserError) Error() string { return e.msg }

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func gen_key() []byte {
    master_key := make([]byte, 16)
    _, err := crand.Read(master_key)
    check(err)
    return master_key
}

var answers []uint32

func load_answers() {
    contents, err := ioutil.ReadFile("colors.txt")
    check(err)
    lines := strings.Split(string(contents), "\n")
    answers = make([]uint32, len(lines) - 1)
    for _, line := range lines {
        if len(line) == 0 {
            continue
        }
        words := strings.Split(line, ": ")
        if len(words) != 2 {
            panic(UserError{"Bad colors format!"})
        }
        vertex, err := strconv.ParseUint(words[0], 10, 32)
        check(err)
        color, err := strconv.ParseUint(words[1], 10, 32)
        check(err)
        // Colors are in the set {1,2,3}
        if color < 1 || color > 3 {
            panic(UserError{"Invalid color for vertex!"})
        }
        answers[vertex] = uint32(color)
    }
}

func get_key(master cipher.Block, ctr uint64) (cipher.Block, []byte) {
    plain := make([]byte, 16)
    new_key := make([]byte, 16)
    binary.BigEndian.PutUint64(plain, ctr)
    master.Encrypt(new_key, plain)
    new_cipher, err := aes.NewCipher(new_key)
    check(err)
    return new_cipher, new_key
}

// knuth shuffles via wikipedia
func rand_perm(n int) []int {
    perm := make([]int, n)
    for i := 0 ; i < n ; i++ {
        j := mrand.Intn(i+1)
        perm[i] = perm[j]
        perm[j] = i
    }
    return perm
}

func send_colors(c cipher.Block, ctr_start uint64, conn net.Conn) {
    plain := make([]byte, 16)
    cipher := make([]byte, 16)
    // Randomly permute the colors
    colors := rand_perm(3)
    for vertex, color := range answers {
        plain[0] = 1 + byte(colors[color - 1])
        plain[15] = 0xFF
        plain[11] = 0xFF
        vertex_cipher, _ := get_key(c, ctr_start + uint64(vertex))
        vertex_cipher.Encrypt(cipher, plain)
        _, err := conn.Write(cipher)
        check(err)
    }
}

func get_challenge(conn net.Conn) (uint32, uint32){
    buf := make([]byte, 4)
    _, err := io.ReadFull(conn, buf)
    check(err)
    v1 := binary.BigEndian.Uint32(buf)
    if v1 >= uint32(len(answers)) {
        panic(UserError{"Invalid vertex indices"})
    }
    _, err = io.ReadFull(conn, buf)
    check(err)
    v2 := binary.BigEndian.Uint32(buf)
    if v2 >= uint32(len(answers)) {
        panic(UserError{"Invalid vertex indices"})
    }
    return v1, v2
}

func send_keys(c cipher.Block, ctr_start uint64, conn net.Conn, v1 uint32, v2 uint32) {
    _, key1 := get_key(c, ctr_start + uint64(v1))
    _, key2 := get_key(c, ctr_start + uint64(v2))
    conn.Write(key1)
    conn.Write(key2)
}

func handle_connection(master_cipher cipher.Block, ctr_start uint64, conn net.Conn) {
    defer func() {
        e := recover()
        if e != nil {
            if uerr, ok := e.(UserError); ok {
                conn.Write([]byte(uerr.Error()))
            }
        }
        conn.Close()
    }()

    for {
        // Send the colors
        send_colors(master_cipher, ctr_start, conn)
        // Receive a challenge (pair of vertices)
        v1, v2 := get_challenge(conn)
        // Return their aes keys
        send_keys(master_cipher, ctr_start, conn, v1, v2)
    }
}

func accept_connections() {
    master_key := gen_key()
    listener, err := net.Listen("tcp", ":8000")
    check(err)
    defer listener.Close()
    var ctr uint64 = 0
    for {
        conn, err := listener.Accept()
        check(err)
        master_cipher, err := aes.NewCipher(master_key)
        check(err)
        go handle_connection(master_cipher, ctr, conn)
        ctr += uint64(len(answers) * 4 + 1);
    }
}

func main() {
    load_answers()
    fmt.Println("Ready to rumble.")
    accept_connections()
}
