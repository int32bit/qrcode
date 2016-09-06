## Quick Start

Pull this image to local:

```
docker pull krystism/qrcode
```


Generate A QR code:

```
docker run -t -i --rm -v `pwd`:/root krystism/qrcode encode --data "Hello World!" -o helloworld.png
```

Output:

![hello world](https://raw.githubusercontent.com/int32bit/qrcode/master/helloworld.png)

Parse a QR code:

```
docker run -t -i --rm -v `pwd`:/root krystism/qrcode decode --file helloworld.png
```

Output：

```
Hello World!
```

Show usage:

```
usage: ./qr [-v] <subcommand> ...

A python app for creating and decoding QR Codes

positional arguments:
  <subcommand>
    bash-completion
    decode         Decode a qrcode, return the data.
    encode         Generate qrcode for the given data.
    help           Display help about this program or one of its subcommands.

optional arguments:
  -v, --version    show program's version number and exit

See "qrcode help COMMAND" for help on a specific comand.
```

## How to Build this image ?

```
git clone https://github.com/int32bit/qrcode.git
cd qrcode
docker build -t krystism/qrcode .
```
