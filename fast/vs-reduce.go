package main

import "strings"
import "os"
import "bufio"
import "fmt"
import "strconv"

//import "flag"

func main() {
	counter := make(map[string]int32)
	//counterf := make(map[string]float64)

	reader := bufio.NewReader(os.Stdin)

	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		line = strings.TrimSpace(line)
		idx := strings.LastIndex(line, "\t")
		if idx != -1 {
			key := line[:idx]
			val_s := line[idx+1:]
			val_i, ierr := strconv.ParseInt(val_s, 0, 32)
			if ierr == nil {
				counter[key] += int32(val_i)
			}

		}
	}

	for k := range counter {
		fmt.Println(k, "\t", counter[k])
	}

}
