import rocksdb
from hexbytes import HexBytes
from iavl.iavl import NodeDB, Tree


def test_basic_ops(tmp_path):
    """
    the expected root hashes are generated by equivalent golang code:
    $ go run ./ref.go
    """
    dbpath = tmp_path / "basic_ops"
    dbpath.mkdir()
    print("db", dbpath)
    exp_root_hashes = [
        None,
        HexBytes("6032661AB0D201132DB7A8FA1DA6A0AFE427E6278BD122C301197680AB79CA02"),
        HexBytes("457D81F933F53E5CFB90D813B84981AA2604D69939E10C94304D18287DED31F7"),
        HexBytes("C7AB142752ADD0374992261536E502851CE555D243270D3C3C6B77CF31B7945D"),
        HexBytes("D6D9F6CA091FA4BD3545F0FEDB2C5865D42123B222C202DF72EFB4BFD75CC118"),
        HexBytes("585581060957AE2E6157F1790A88BF3544FECC9902BBF2E2286CF7325539126C"),
        HexBytes("AB4C3DEFB7266D7587BAEA808B0BA2D74C294A96D55BDA7AB5E473CD75BC8E64"),
    ]
    kvdb = rocksdb.DB(str(dbpath), rocksdb.Options(create_if_missing=True))
    db = NodeDB(kvdb)
    tree = Tree(db, 0)
    assert not tree.set(b"hello", b"world")
    assert exp_root_hashes[1] == tree.save_version()

    tree = Tree(db, 1)
    assert b"world" == tree.get(b"hello")
    assert tree.set(b"hello", b"world1")
    assert not tree.set(b"hello1", b"world1")
    assert exp_root_hashes[2] == tree.save_version()

    tree = Tree(db, 2)
    assert b"world1" == tree.get(b"hello")
    assert b"world1" == tree.get(b"hello1")
    tree.set(b"hello2", b"world1")
    tree.set(b"hello3", b"world1")
    assert exp_root_hashes[3] == tree.save_version()

    tree = Tree(db, 3)
    assert b"world1" == tree.get(b"hello3")

    node = db.get(db.get_root_hash(3))
    assert 2 == node.height

    for i in range(20):
        tree.set(b"hello%02d" % i, b"world1")
    assert exp_root_hashes[4] == tree.save_version()

    # remove nothing
    assert tree.remove(b"not exists") is None

    tree.remove(b"hello")
    tree.remove(b"hello19")
    h = tree.save_version()
    assert not tree.get(b"hello")
    assert exp_root_hashes[5] == h

    # try to cover all balancing cases
    for i in range(11):
        tree.set(b"aello%02d" % i, b"world1")
    for i in range(20, 10, -1):
        tree.set(b"aello%02d" % i, b"world1")
    assert exp_root_hashes[6] == tree.save_version()

    # test cache miss
    db = NodeDB(kvdb)
    tree = Tree(db)
    assert tree.version == len(exp_root_hashes) - 1
    assert b"world1" == tree.get(b"aello20")


def test_empty_tree(tmp_path):
    dbpath = tmp_path / "empty-tree"
    dbpath.mkdir()
    db = NodeDB(rocksdb.DB(str(dbpath), rocksdb.Options(create_if_missing=True)))

    tree = Tree(db)
    assert tree.version == 0

    tree = Tree(db, 0)
    assert tree.get("hello") is None
    assert tree.remove("hello") is None
    tree.save_version()
    assert tree.version == 1
