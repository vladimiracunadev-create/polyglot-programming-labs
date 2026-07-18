package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	viejo, nuevo := n*2, n+n
	res := "false"
	if viejo == nuevo {
		res = "true"
	}
	fmt.Printf("equivalente=%s resultado=%d\n", res, nuevo)
}
