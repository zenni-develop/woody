"""Minimal brotli shim backed by Node's zlib, for fontTools WOFF2 only."""
import subprocess
_JS_C = "const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d));process.stdin.on('end',()=>{const o={};o[z.constants.BROTLI_PARAM_MODE]=+process.argv[1];o[z.constants.BROTLI_PARAM_QUALITY]=+process.argv[2];o[z.constants.BROTLI_PARAM_LGWIN]=+process.argv[3];o[z.constants.BROTLI_PARAM_SIZE_HINT]=Buffer.concat(c).length;process.stdout.write(z.brotliCompressSync(Buffer.concat(c),{params:o}))})"
_JS_D = "const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d));process.stdin.on('end',()=>process.stdout.write(z.brotliDecompressSync(Buffer.concat(c))))"
MODE_GENERIC, MODE_TEXT, MODE_FONT = 0, 1, 2
def compress(data, mode=0, quality=11, lgwin=22, lgblock=0):
    return subprocess.run(["node", "-e", _JS_C, str(mode), str(quality), str(lgwin)], input=bytes(data), capture_output=True, check=True).stdout
def decompress(data):
    return subprocess.run(["node", "-e", _JS_D], input=bytes(data), capture_output=True, check=True).stdout
error = Exception
