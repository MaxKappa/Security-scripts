package main

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
	"io"
	"os"
)

// Encrypter is the main struct of the package
type Encrypter struct {
	// Key is the key used to encrypt the file
	Key []byte
	// File is the file to be encrypted
	File *os.File
	// EncryptedFile is the encrypted file
	EncryptedFile *os.File
}

// NewEncrypter returns a new Encrypter struct
func NewEncrypter(key []byte, file *os.File) *Encrypter {
	return &Encrypter{
		Key:           key,
		File:          file,
		EncryptedFile: nil,
	}
}

// Encrypt encrypts the file
func (e *Encrypter) Encrypt() error {
	// Open the file to be encrypted
	file, err := os.Open(e.File.Name())
	if err != nil {
		return err
	}
	defer file.Close()

	encrypt(file, e.Key)
	//walker.RenameFile(e.File.Name())
	return nil
}

func encrypt(file *os.File, key []byte) error {
	b := bufio.NewScanner(file)
	for b.Scan() {
		plaintext := []byte(b.Text())
		block, err := aes.NewCipher(key)
		if err != nil {
			return err
		}
		gcm, err := cipher.NewGCM(block)
		if err != nil {
			return err
		}
		nonce := make([]byte, gcm.NonceSize())
		if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
			return err
		}
		ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
		//Write ciphertext to open file
		_, err = file.Write(ciphertext)
		if err != nil {
			return err
		}
		return nil
	}
	return nil
}

func main() {
	key := []byte("example key 1234")
	file, err := os.Open("test.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	e := NewEncrypter(key, file)
	err = e.Encrypt()
	if err != nil {
		fmt.Println(err)
	}
}
