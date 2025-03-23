import hmac
import hashlib
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak


class HDWallet:
    """分层确定性钱包(支持BIP-32/BIP-44)
    Args:
        seed (bytes): 主种子(至少128位)
    Example:
        >>> seed = b'\x12\x34...'
        >>> wallet = HDWallet(seed)
        >>> wallet.derive_path("m/44'/60'/0'/0/0")
        '0x...'
    """

    def __init__(self, seed):
        self.master_private_key, self.chain_code = self._generate_master_key(seed)

    def _generate_master_key(self, seed):
        """生成主密钥(BIP-32)
        Args:
            seed (bytes): 输入种子
        Returns:
            tuple: (private_key, chain_code)
        """
        hmac_result = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
        return hmac_result[:32], hmac_result[32:]

    def _derive_child_key(self, parent_key, chain_code, index, hardened=False):
        """派生单个子密钥
        Args:
            parent_key (bytes): 父私钥
            chain_code (bytes): 父链码
            index (int): 派生索引
            hardened (bool): 是否为硬化派生
        """
        if hardened:
            data = b"\x00" + parent_key + index.to_bytes(4, "big")
        else:
            raise NotImplementedError("仅支持硬化派生")

        hmac_result = hmac.new(chain_code, data, hashlib.sha512).digest()
        child_key = hmac_result[:32]
        new_chain_code = hmac_result[32:]
        return child_key, new_chain_code

    def derive_path(self, path):
        """根据BIP-44路径派生密钥
        Args:
            path (str): 派生路径(如 m/44'/60'/0'/0/0)
        Returns:
            str: 以太坊地址
        """
        indices = self._parse_path(path)
        current_key = self.master_private_key
        current_chain = self.chain_code

        for index in indices:
            current_key, current_chain = self._derive_child_key(
                current_key, current_chain, index, hardened=(index >= 0x80000000)
            )

        return self._generate_address(current_key)

    def _parse_path(self, path):
        """解析BIP-44路径
        Args:
            path (str): 路径字符串
        Returns:
            list: 索引列表
        Example:
            >>> _parse_path("m/44'/60'/0'/0/0")
            [2147483692, 2147483708, 2147483648, 0, 0]
        """
        if not path.startswith("m"):
            raise ValueError("路径必须以m开头")
        return [self._parse_index(part) for part in path.split("/")[1:]]

    def _parse_index(self, index_str):
        """解析路径中的索引"""
        if "'" in index_str:
            return int(index_str[:-1]) + 0x80000000
        return int(index_str)

    def _generate_address(self, private_key):
        """从私钥生成地址"""
        sk = SigningKey.from_string(private_key, curve=SECP256k1)
        public_key = sk.get_verifying_key().to_string("uncompressed")

        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(public_key[1:])
        return "0x" + keccak_hash.digest()[-20:].hex()


# -------------------- 执行 --------------------
if __name__ == "__main__":
    # 生成种子
    seed = b"\x1a\xf2\x8c..."  # 实际应使用安全随机数
    # 创建HD钱包
    wallet = HDWallet(seed)
    # 派生标准以太坊路径
    address1 = wallet.derive_path("m/44'/60'/0'/0/0")
    print("地址1:", address1)
    # 派生下一个地址
    address2 = wallet.derive_path("m/44'/60'/0'/0/1")
    print("地址2:", address2)
