package decrypter

import (
	"bufio"
	"crypto/aes"
	"crypto/cipher"
	"os"
)

// Decrypter is the main struct of the package
type Decrypter struct {
	// Key is the key used to decrypt the file
	Key []byte
	// File is the file to be decrypted
	File *os.File
	// DecryptedFile is the decrypted file
	DecryptedFile *os.File
}

// NewDecrypter returns a new Decrypter struct
func NewDecrypter(key []byte, file *os.File) *Decrypter {
	return &Decrypter{
		Key:           key,
		File:          file,
		DecryptedFile: nil,
	}
}

// Decrypt decrypts the file
func (d *Decrypter) Decrypt() error {
	// Open the file to be decrypted
	file, err := os.Open(d.File.Name())
	if err != nil {
		return err
	}
	defer file.Close()

	decrypt(file, d.Key)
	//walker.RenameFile(d.File.Name())
	return nil
}

func decrypt(file *os.File, key []byte) error {
	b := bufio.NewScanner(file)
	for b.Scan() {
		ciphertext := []byte(b.Text())
		block, err := aes.NewCipher(key)
		if err != nil {
			return err
		}
		gcm, err := cipher.NewGCM(block)
		if err != nil {
			return err
		}
		nonceSize := gcm.NonceSize()
		nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]
		plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
		if err != nil {
			return err
		}
		_, err = file.Write(plaintext)
		if err != nil {
			return err
		}
	}
	return nil
}
