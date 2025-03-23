# 钱包地址生成过程

- 第一步：生成种子。种子是一个随机生成的数字序列，是后续的起点。种子可以由系统生成的随机数或用户提供的熵（比如随机移动鼠标产生的数据）来产生。
- 第二步：生成助记词。助记词是将种子转换成的一系列方便记忆的单词。在以太坊中，有一个固定的2048个单词的单词库，首先将种子分割成多个二进制数据片段，每一个片段对应单词库中的一个单词，最终形成一串单词序列，即助记词。
- 第三步：生成私钥。私钥是控制钱包地址的密钥。使用上一步的种子，通过 HMAC-SHA512 算法进行计算，可以得到私钥。
- 第四步：生成公钥。有了私钥之后，通过椭圆曲线加密算法（ ECDSA ），我们可以计算出对应的公钥。
- 第五步：生成地址。最后一步是生成钱包地址。首先使用 Keccak-256 哈希函数计算公钥的哈希值，然后取哈希值的最后20个字节，就是一个以太坊钱包地址。

## 注意事项

- 单词库文件 可前往<https://github.com/bitcoin/bips/blob/master>寻找
- 熵长度与助记词数量

```doc
熵长度 校验和 总位数 单词数
128位   4位   132位  12个
256位   8位   264位  24个
```

- 安全性

1. 系统生成方式使用secrets模块，适合生产环境。
2. 用户熵需确保足够随机（真实场景需采集更复杂的用户行为）。

- 私钥保护

1. 私钥一旦泄露，任何人可控制该地址资产。
2. 禁止将私钥或助记词明文存储在网络环境。

- 地址验证
生成的地址可通过[以太坊浏览器](https://etherscan.io/)验证有效性。

### 验证结果

```docs
=== 系统生成流程 ===
种子 (HEX): bb9dea7fdaxxxxxxxxxxxxxxxxxxxx30b9a80bb85d9d245e7d9c66ecd112942
助记词: romance xxxxx xxxxx relief law xxxxx strong lawsuit xxxxxx umbrella process maid xxxxx doctor unlock robot xxxxx connect wait mimic xxxxx mass pink either
私钥 (HEX): 8e51a75ed4xxxxxxxxxxxxxxxxxxxxe2ab9080c56599e92be43c0013a4448017
公钥 (HEX): 048dc28c96xxxxxxxxxxxxxxxxxxxx60eb276e51669220e4a47f05094256c3967c8a1d5f58a980f3a59863d37a767f1f7331333769d568731c6c7c9cda7e9dfe25
地址: 0x9bcc529ee0ab53987d27cf1e4c4626272981e08c
```

![alt text](docs/0x9bcc529ee0ab53987d27cf1e4c4626272981e08c.png)

```docs
=== 用户熵生成流程 ===
种子 (HEX): 180fe62312xxxxxxxxxxxxxxxxxxxxd532e9228ded1cbc3c284f967febf5d1c9
助记词: blossom left xxxxx certain xxxxx history silver jungle cost decrease prepare xxxxx company mule dash xxxxx rotate xxxxx become coconut xxxxx wife xxxxx day
私钥 (HEX): 265cfa742axxxxxxxxxxxxxxxxxxxxb62bc1c99ae5f9224cf4121fe28444dbd4
公钥 (HEX): 04bd96a8f2xxxxxxxxxxxxxxxxxxxxe73cf65f5a1c68d78a2cd20765d162feb4391ed44e0ff5f9beaf366432ea0539b352bdc45a37785fa2787d483ac18c6cd3bf
地址: 0x91d815a7ab7cd221c5a5de0b0f8e5e189381f076
```

![alt text](docs/0x91d815a7ab7cd221c5a5de0b0f8e5e189381f076.png)
