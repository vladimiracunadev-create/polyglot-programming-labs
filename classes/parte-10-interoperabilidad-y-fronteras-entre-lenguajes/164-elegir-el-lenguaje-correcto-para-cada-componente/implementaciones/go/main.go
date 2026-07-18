package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	tipo := strings.TrimSpace(line)
	rec := map[string]string{"sistemas": "Rust", "web": "TypeScript", "datos": "SQL"}
	r, ok := rec[tipo]
	if !ok {
		r = "Python"
	}
	fmt.Printf("lenguaje=%s\n", r)
}
