import os
import secrets
import hashlib
import hmac
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak


# -------------------- 公共工具函数 --------------------
def load_wordlist():
    """加载BIP-39标准英语单词库
    Args:
        无参数
    Returns:
        list: 包含2048个BIP-39标准单词的列表
    Example:
        >>> load_bip39_wordlist()
        ["abandon", "ability", "able", ..., "zone"]
    """
    with open("./bip-0039/english.txt", "r") as f:
        return [word.strip() for word in f.readlines()]


def entropy_to_mnemonic(entropy):
    """从熵生成助记词(BIP-39标准)
    Args:
        entropy (bytes): 输入熵(128/160/192/224/256位的字节数据)
    Returns:
        str: 由空格分隔的助记词字符串
    Example:
        >>> entropy = b'\x12\x34\x56...'
        >>> entropy_to_mnemonic(entropy)
        "apple chaos field ..."
    """
    # 验证熵长度
    entropy_bits = len(entropy) * 8
    if entropy_bits not in [128, 160, 192, 224, 256]:
        raise ValueError("Invalid entropy length. Must be 128/160/192/224/256 bits.")
    # 步骤1：计算校验和
    hash_bytes = hashlib.sha256(entropy).digest()
    checksum_bits = entropy_bits // 32  # 校验和位数
    # 提取校验和(取哈希的第一个字节的高位)
    checksum_byte = hash_bytes[0]
    checksum = format(checksum_byte, "08b")[:checksum_bits]
    # 步骤2：将熵转换为二进制字符串
    entropy_bin = "".join(format(byte, "08b") for byte in entropy)
    # 步骤3：拼接熵和校验和
    combined_bits = entropy_bin + checksum
    # 步骤4：分割为11位的索引
    indices = [
        int(combined_bits[i : i + 11], 2) for i in range(0, len(combined_bits), 11)
    ]
    # 步骤5：映射到单词库
    word_list = load_wordlist()
    return " ".join([word_list[i] for i in indices])


# -------------------- 核心生成逻辑 --------------------
class EthereumWalletGenerator:
    def __init__(self, seed):
        """钱包生成器构造函数
        Args:
            seed (bytes): 二进制种子数据(32字节)
        """
        self.seed = seed  # 种子(二进制数据)
        self.private_key = None
        self.public_key = None
        self.address = None

    def generate_private_key(self):
        """生成私钥(HMAC-SHA512)
        Args:
            无参数
        Returns:
            bytes: 32字节的私钥
        Example:
            >>> private_key = generate_private_key()
            b'\x1a\xf2\x8c...'
        """
        # 使用BIP-32标准生成主私钥(key="Bitcoin seed", 数据=seed)
        hmac_result = hmac.new(b"Bitcoin seed", self.seed, hashlib.sha512).digest()
        # 前32字节为私钥，后32字节为链码(chain code)
        self.private_key = hmac_result[:32]
        return self.private_key

    def generate_public_key(self):
        """从私钥生成公钥(ECDSA-secp256k1)
        Args:
            无参数
        Returns:
            bytes: 65字节的非压缩格式公钥
        Example:
            >>> public_key = generate_public_key()
            b'\x04\xd0\xb1...'
        """
        sk = SigningKey.from_string(self.private_key, curve=SECP256k1)
        self.public_key = sk.get_verifying_key().to_string("uncompressed")
        return self.public_key

    def generate_address(self):
        """生成以太坊地址(Keccak-256)
        Args:
            无参数
        Returns:
            str: 以太坊地址字符串(0x开头)
        Example:
            >>> generate_address()
            "0x5a1f3c8d0e9b2a7f5c6d3e8a1b0f2e5d7c4b6a9e"
        """
        # 计算Keccak-256哈希(注意以太坊用未压缩公钥且去掉首字节0x04)
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(self.public_key[1:])  # 去掉开头的04
        address_bytes = keccak_hash.digest()[-20:]  # 取最后20字节
        self.address = "0x" + address_bytes.hex()
        return self.address


# -------------------- 系统生成助记词 --------------------
"""
系统生成流程
1.生成熵
使用secrets.token_bytes(32)生成256位(32字节)密码学安全随机数。
2.计算校验和
对熵进行SHA-256哈希运算,取哈希值的第一个字节(8位)作为校验和。
3.二进制拼接
将256位熵(二进制字符串)与8位校验和拼接,形成264位数据。
4.生成助记词
将264位数据按11位一组分割,得到24个索引值。
每个索引对应BIP-39单词库中的特定单词。

=== 系统生成种子 → 助记词 ===
系统种子 (HEX): 5a1fe3d8...(64位十六进制)
助记词 (24个单词):
ability cancel safe ...(共24个单词)
"""


def system_generate():
    """执行系统生成完整流程
    Args:
        无参数
    Returns:
        无返回值
    Example:
        >>> system_generate()
        === 系统生成流程 ===
        种子 (HEX): 4a1f3c8d0e...
        助记词: ability cancel safe ...
        私钥 (HEX): 3a7d8f...
        公钥 (HEX): 04d0b1c8...
        地址: 0x5a1f3c8d...
    """
    print("\n=== 系统生成流程 ===")
    # 生成种子(32字节)
    seed = secrets.token_bytes(32)
    print("种子 (HEX):", seed.hex())
    # 生成助记词
    mnemonic = entropy_to_mnemonic(seed)
    print("助记词:", mnemonic)
    # 生成钱包
    wallet = EthereumWalletGenerator(seed)
    private_key = wallet.generate_private_key()
    print("私钥 (HEX):", private_key.hex())
    public_key = wallet.generate_public_key()
    print("公钥 (HEX):", public_key.hex())
    address = wallet.generate_address()
    print("地址:", address)


# -------------------- 用户熵生成助记词 --------------------
"""
用户熵生成流程
1.集用户熵
模拟用户输入(如100个鼠标坐标),转换为字节数据。
2.生成种子
对用户熵进行SHA-256哈希,得到32字节的确定性种子。
3.后续步骤
校验和计算、二进制拼接和助记词生成逻辑与系统生成流程完全相同。
"""


def user_generate():
    """执行用户熵生成完整流程
    Args:
        无参数
    Returns:
        无返回值
    Example:
        >>> user_generate()
        === 用户熵生成流程 ===
        种子 (HEX): 8c3a5f1e...
        助记词: castle defense ...
        私钥 (HEX): 5d6e7f...
        公钥 (HEX): 04a3b4c5...
        地址: 0x8c3a5f1e...
    """
    print("\n=== 用户熵生成流程 ===")
    # 模拟用户熵(鼠标移动)
    user_entropy = str(
        [(secrets.randbelow(1000), secrets.randbelow(1000)) for _ in range(100)]
    ).encode()
    seed = hashlib.sha256(user_entropy).digest()
    print("种子 (HEX):", seed.hex())
    # 生成助记词
    mnemonic = entropy_to_mnemonic(seed)
    print("助记词:", mnemonic)
    # 生成钱包
    wallet = EthereumWalletGenerator(seed)
    private_key = wallet.generate_private_key()
    print("私钥 (HEX):", private_key.hex())
    public_key = wallet.generate_public_key()
    print("公钥 (HEX):", public_key.hex())
    address = wallet.generate_address()
    print("地址:", address)


# -------------------- 执行 --------------------
if __name__ == "__main__":
    system_generate()  # 执行系统生成流程
    user_generate()  # 执行用户生成流程
