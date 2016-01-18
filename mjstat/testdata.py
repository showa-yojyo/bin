# -*- coding: utf-8 -*-
"""testdata.py:
"""

test_input = r'''===== 東風戦：ランキング卓 64卓 開始 2016/01/01 00:43 =====
  持点25000 [1]あなた R1500 [2]下家 R1500 [3]対面 R1500 [4]上家 R1500
  東1局 0本場(リーチ0) 対面 2600 上家 -2600 
    40符 二飜ロン 断ヤオ リーチ
    [1北]1m2m5m9m1p3p7p7p8p1s4s4s東
    [2東]1m2m4m8m2p5p1s7s7s南北白発
    [3南]1m4m7m9m2p2p8p5s8s8s9s中中
    [4西]7m8m1p3p3p4p9p4s7s9s西北発
    [表ドラ]西 [裏ドラ]3s
    * 2G8m 2d南 3G9p 3d1m 4G西 4d北 1G8p 1d1s 2G9p 2d北 3G7m 3d4m 4G6m 4d発
    * 1G1s 1d9m 2G5m 2d発 3G3s 3d中 4G2s 4d9p 1G1m 1d1s 2G西 2d白 3G4m 3d中
    * 4G1p 4d2s 1G中 1D中 2G3s 2d9p 3G7m 3d9m 4G5s 4d9s 1G発 1D発 2G2s 2d西 4N
    * 4d7s 1G6p 1d東 2G6s 2d2p 3G5m 3d9p 4G9s 4D9s 1G6s 1d4s 2G4m 2d5p 3G6p
    * 3d3s 4C4s5s 4d3p 1G白 1d3p 2G1s 2d2s 3G9m 3d9s 4G東 4D東 1G2m 1d白 2G2m
    * 2d7s 3G2p 3d9m 4G6s 4D6s 1G5p 1d6s 2G9m 2d6s 3G6m 3R 3d5s 4G8m 4D8m 1G南
    * 1D南 2G4p 2d8m 3G6m 3D6m 4G白 4D白 1G6p 1d1m 2G8p 2d1m 3G東 3D東 4G3p
    * 4D3p 1G1p 1d1m 2G東 2D東 3G3s 3D3s 4G9s 4D9s 1G北 1D北 2G4p 2d8m 3G6m
    * 3D6m 4G7p 4D7p 3A

  東2局 0本場(リーチ0) 上家 13000 あなた -3000 下家 -4000 対面 -6000 
    ハネ満貫ツモ 断ヤオ 門前清模和 リーチ 一発 ドラ2
    [1西]5m2p4p9p6s6s7s7s9s東白発発
    [2北]1m7m8m5p7p7p8p9p3s5s8s東東
    [3東]4m6m9m3p3p5p6p7p南西白発中
    [4南]2m3m3m4m1p3p4p6p9p2s2s4s5s
    [表ドラ]4s [裏ドラ]6m
    * 3G中 3d南 4G北 4D北 1G西 1d9p 2G3m 2d8s 3G9s 3d西 4G北 4D北 1G7m 1d西
    * 2G9m 2d7p 3G6m 3d白 4G5p 4d9p 1G南 1D南 2G4s 2R 2d5p 3G2s 3d5p 4G北 4D北
    * 1G1s 1d白 2G6s 2D6s 3G7s 3d7p 4G8p 4d5p 1G2p 1d9s 2G8s 2D8s 3G2m 3d9s
    * 4G3p 4d8p 1G8m 1d6s 2G南 2D南 3G8m 3d中 4G6p 4d3p 1G1m 1d6s 2G1m 2D1m
    * 3G4p 3d中 4G2s 4d3p 1G4s 1d1m 2G9s 2D9s 3G7p 3d3p 4G4s 4d4p 1G南 1d4p
    * 2G2p 2D2p 3G1s 3d3p 4G6s 4d1p 1G9m 1d南 2G4p 2D4p 3G西 3d4p 4G1p 4D1p
    * 1G4m 1d2p 2G8p 2D8p 3G西 3d7p 4G3s 4R 4d3m 1G発 1d2p 2G6m 2D6m 3G2p 3D2p
    * 4G6p 4A

  東3局 0本場(リーチ0) 対面 2000 上家 -2000 
    30符 一飜ロン 発
    [1南]1m3m5m3p4p6p1s3s6s7s南西発
    [2西]5m5m9m3p4p1s2s3s7s9s東西中
    [3北]2m6m4p9p9p4s5s8s8s北発発中
    [4東]2m4m6m1p2p5p7p8p5s8s西白発
    [表ドラ]白 [裏ドラ]2m
    * 4G8m 4d西 1G2p 1d西 2G2s 2d西 3G1s 3d中 4G3p 4d発 3N 3d北 4G6m 4d白 1G7m
    * 1d発 2G9s 2d中 3G1m 3d1s 4G7m 4d8s 3N 3d6m 4G2p 4d5s 1G白 1d南 2G4m 2d東
    * 3G2s 3D2s 4G4m 4d2m 1G7p 1d1m 2G4p 2d9m 3G6s 3d4p 4G4s 4d2p 1G1p 1D1p
    * 2G東 2D東 3G6s 3D6s 4G5m 4d4s 1G1p 1D1p 2G5p 2d2s 3G8m 3D8m 4G9s 4D9s
    * 1G7s 1D7s 2G8m 2d7s 3G白 3D白 4G9m 4d5p 1G6m 1d白 2G4s 2d8m 3G北 3D北
    * 4G2s 4D2s 1G3m 1d1s 2G東 2D東 3G1p 3D1p 4G5p 4D5p 1C6p7p 1d3s 2G8m 2D8m
    * 3G南 3D南 4G7p 4R 4d8p 1G2p 1D2p 2G8p 2D8p 3G北 3D北 4G中 4D中 1G6p 1d2p
    * 2G9m 2d2s 3G8p 3D8p 4G5s 4D5s 1G9p 1d7s 2G7m 2d9s 3G5p 3D5p 4G7m 4D7m
    * 1G7s 1d7m 2G6p 2d7m 3G9m 3D9m 4G3m 4D3m 3A

  東4局 0本場(リーチ0) あなた 4900 対面 -4900 
    40符 二飜ロン リーチ ドラ1
    [1東]3m4m9m6p6p8p2s6s6s8s南白発
    [2南]6m6m9m2p8p1s2s4s5s6s東北北
    [3西]1m9m1p1p2p2p5p1s4s4s5s6s北
    [4北]1m1m3m3m3m6p7p7p3s7s東西中
    [表ドラ]9m [裏ドラ]5m
    * 1G中 1d南 2G4m 2d東 3G7m 3d北 4G5s 4d東 1G6p 1d9m 2G7m 2d2p 3G西 3D西
    * 4G4p 4d西 1G2p 1D2p 2G3s 2d8p 3G7m 3d1s 4G5p 4d中 1G6m 1d中 2G7s 2d4s
    * 3G8m 3d1m 4G北 4D北 1G南 1D南 2G9s 2D9s 3G3p 3d7m 4G3p 4d7p 1G7s 1d白
    * 2G7p 2D7p 3G3p 3R 3d5p 4G9s 4d1m 1G7p 1d発 2G東 2D東 3G西 3D西 4G中 4d1m
    * 1G5p 1d2s 2G9p 2D9p 3G3p 3D3p 4G白 4d3p 1G5m 1d3m 2G4p 2d6m 3G南 3D南
    * 4G9m 4d3m 1G9s 1R 1d5p 2G8s 2d2s 3G2m 3D2m 4G8p 4d3m 1G8s 1D8s 2G7m 2d8s
    * 3G1p 3D1p 4G9p 4d3m 1G1m 1D1m 2G発 2D発 3G白 3D白 4G9p 4d白 1G5m 1D5m
    * 2G8m 2d北 3G9p 3D9p 1A

  東4局 1本場(リーチ0) 下家 1300 対面 -1300 
    30符 一飜ロン 断ヤオ
    [1東]1m2m4m7m1p1s4s4s9s北北北発
    [2南]7m8m8m9m2p4p7p7p9p4s5s5s5s
    [3西]2m4m5m3p6p8p9p東西白発中中
    [4北]3m6m8m3p3p4p1s2s8s9s9s東中
    [表ドラ]9p [裏ドラ]8m
    * 1G3s 1d1p 2G2s 2d9p 3G6p 3d東 4G8p 4d東 1G2p 1d9s 2G6p 2d8m 3G白 3d発
    * 4G南 4D南 1G6m 1d発 2G発 2D発 3G5s 3d西 4G発 4D発 1G4s 1d1m 2G9m 2D9m
    * 3G5m 3d2m 4G1p 4d中 1G7m 1d2p 2G1p 2D1p 3G南 3D南 4G9m 4D9m 1G西 1D西
    * 2G7s 2D7s 3G南 3D南 4G5m 4d1p 1G3m 1d6m 2G9p 2D9p 3G6p 3d3p 4G1m 4d8m
    * 1G3s 1d1s 2G7s 2D7s 3G3s 3d5s 4G2s 4d8p 1G8p 1D8p 2G2p 2d4p 3G5m 3d4m
    * 4G2m 4d3p 1G6s 1D6s 2G1m 2D1m 3G5p 3D5p 4G5p 4d8s 1G8s 1D8s 2G西 2D西
    * 3G7s 3D7s 4G東 4D東 1G6s 1D6s 2G6m 2d9m 3G6s 3D6s 4G2m 4D2m 1G1s 1D1s
    * 2G4p 2D4p 3G4m 3D4m 4G7p 4D7p 2N 2d6p 3G東 3D東 4G2p 4D2p 1G1p 1D1p 2G中
    * 2D中 3N 3d3s 2A

  ---- 試合結果 ----
  1位 上家          +54
  2位 あなた        +7
  3位 下家          -18
  4位 対面          -43
----- 64卓 終了 2016/01/01 00:47 -----

'''
