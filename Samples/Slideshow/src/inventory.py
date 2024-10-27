assets = {
    "RenderGroup": {
        "class_name": "RenderGroup",
        "kwargs": {
        }
    },
    "LayerManager": {
        "class_name": "LayerManager",
        "kwargs": {
            "layers": [
                ["Photo"],
            ]
        }
    },
    "fast_hand_font": {
        "class_name": "FontAsset",
        "kwargs": {
            "font:fname": "fast-hand-font/FastHand-lgBMV.ttf",
            "size": 42
        }
    }
}

game_types = {
    "Slideshow": {
        "class_name": "Slideshow",
        "kwargs": {
            "asset:render_group": "RenderGroup",
            "game_object:collision_manager": "CollisionManager",
            "game_object:photo_spawner": "/PhotoSpawner",
        },
        "CollisionManager": {
            "class_name": "CollisionManager",
            "kwargs": {
                "asset:collision_checks": [
                ]
            }
        }
    },
    "PhotoSpawner": {
        "class_name": "PhotoSpawner",
        "kwargs": {
            "type_spec:photo_type_spec": "Photo",
            "spawn_freq": 1000,
            "image:images": [
                "000",
                "001",
                "002",
                "003",
                "004",
                "005",
                "006",
                "007",
                "008",
                # "009",
                # "010",
                # "011",
                # "012",
                # "013",
                # "014",
                # "015",
                # "016",
                # "017",
                # "018",
                # "019",
                # "020",
                # "021",
                # "022",
                # "023",
                # "024",
                # "025",
                # "026",
                # "027",
                # "028",
                # "029",
                # "030",
                # "031",
                # "032",
                # "033",
                # "034",
                # "035",
                # "036",
                # "037",
                # "038",
                # "039",
                # "040",
                # "041",
                # "042",
                # "043",
                # "044",
                # "045",
                # "046",
                # "047",
                # "048",
                # "049",
                # "050",
                # "051",
                # "052",
                # "053",
                # "054",
                # "055",
                # "056",
                # "057",
                # "058",
                # "059",
                # "060",
                # "061",
                # "062",
                # "063",
                # "064",
                # "065",
                # "066",
                # "067",
                # "068",
                # "069",
                # "070",
                # "071",
                # "072",
                # "073",
                # "074",
                # "075",
                # "076",
                # "077",
                # "078",
                # "079",
                # "080",
                # "081",
                # "082",
                # "083",
                # "084",
                # "085",
                # "086",
                # "087",
                # "088",
                # "089",
                # "090",
                # "091",
                # "092",
                # "093",
                # "094",
                # "095",
                # "096",
                # "097",
                # "098",
                # "099",
                # "100",
                # "101",
                # "102",
                # "103",
                # "104",
                # "105",
                # "106",
                # "107",
                # "108",
                # "109",
                # "110",
                # "111",
                # "112",
                # "113",
                # "114",
                # "115",
                # "116",
                # "117",
                # "118",
                # "119",
                # "120",
                # "121",
                # "122",
                # "123",
                # "124",
                # "125",
                # "126",
                # "127",
                # "128",
                # "129",
                # "130",
                # "131",
                # "132",
                # "133",
                # "134",
                # "135",
                # "136",
                # "137",
                # "138",
                # "139",
                # "140",
                # "141",
                # "142",
                # "143",
                # "144",
                # "145",
                # "146",
                # "147",
                # "148",
                # "149",
                # "150",
                # "151",
                # "152",
                # "153",
                # "154",
                # "155",
                # "156",
                # "157",
                # "158",
                # "159",
                # "160",
                # "161",
                # "162",
                # "163",
                # "164",
                # "165",
                # "166",
                # "167",
                # "168",
                # "169",
                # "170",
                # "171",
                # "172",
                # "173",
                # "174",
                # "175",
                # "176",
                # "177",
                # "178",
                # "179",
                # "180",
                # "181",
                # "182",
                # "183",
                # "184",
                # "185",
                # "186",
                # "187",
                # "188",
                # "189",
                # "190",
                # "191",
                # "192",
                # "193",
                # "194",
                # "195",
                # "196",
                # "197",
                # "198",
                # "199",
                # "200",
                # "201",
                # "202",
                # "203",
                # "204",
                # "205",
                # "206",
                # "207",
                # "208",
                # "209",
                # "210",
                # "211",
                # "212",
                # "213",
                # "214",
                # "215",
                # "216",
                # "217",
                # "218",
                # "219",
                # "220",
                # "221",
                # "222",
                # "223",
                # "224",
                # "225",
                # "226",
                # "227",
                # "228",
                # "229",
                # "230",
                # "231",
                # "232",
                # "233",
                # "234",
                # "235",
                # "236",
                # "237",
                # "238",
                # "239",
                # "240",
                # "241",
                # "242",
                # "243",
                # "244",
            ],
            "asset:render_group": "RenderGroup",
        }
    },
    "Photo": {
        "class_name": "Photo",
        "kwargs": {
            "game_object:mover": "PhotoMover",
            "kill_when_off_screen": True
        },
        "groups": [
            "RenderGroup",
        ],
        "PhotoMover": {
            "class_name": "MoverVelDir",
            "kwargs": {
                "velocity": 50.0,
                "direction": [0, 1]
            }
        }
    },
}

images = {
    "000": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_081700.jpg",
    "001": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_162400.jpg",
    "002": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_171900.jpg",
    "003": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_171928.jpg",
    "004": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_171942.jpg",
    "005": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_172400.jpg",
    "006": "/Users/ernie/Downloads/Tete_photos_fixed_names/19660101_172600.jpg",
    "007": "/Users/ernie/Downloads/Tete_photos_fixed_names/19661027_181500.jpg",
    "008": "/Users/ernie/Downloads/Tete_photos_fixed_names/19661227_171400.jpg",
    # "009": "/Users/ernie/Downloads/Tete_photos_fixed_names/19661227_171401.jpg",
    # "010": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670101_172014.jpg",
    # "011": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670101_172032.jpg",
    # "012": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670101_172136.jpg",
    # "013": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670101_172148.jpg",
    # "014": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670101_172818.jpg",
    # "015": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670201_172600.jpg",
    # "016": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670201_172630.jpg",
    # "017": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670201_172638.jpg",
    # "018": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670201_172700.jpg",
    # "019": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_173200.jpg",
    # "020": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_173204.jpg",
    # "021": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_173548.jpg",
    # "022": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_173836.jpg",
    # "023": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_173856.jpg",
    # "024": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_174220.jpg",
    # "025": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_174254.jpg",
    # "026": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_174310.jpg",
    # "027": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_174312.jpg",
    # "028": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_174406.jpg",
    # "029": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670401_174644.jpg",
    # "030": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670801_192100.jpg",
    # "031": "/Users/ernie/Downloads/Tete_photos_fixed_names/19670801_193210.jpg",
    # "032": "/Users/ernie/Downloads/Tete_photos_fixed_names/19671201_180200.jpg",
    # "033": "/Users/ernie/Downloads/Tete_photos_fixed_names/19671201_180204.jpg",
    # "034": "/Users/ernie/Downloads/Tete_photos_fixed_names/19671201_180226.jpg",
    # "035": "/Users/ernie/Downloads/Tete_photos_fixed_names/19680428_185900.jpg",
    # "036": "/Users/ernie/Downloads/Tete_photos_fixed_names/19680428_190018.jpg",
    # "037": "/Users/ernie/Downloads/Tete_photos_fixed_names/19680501_185800.jpg",
    # "038": "/Users/ernie/Downloads/Tete_photos_fixed_names/19680501_185848.jpg",
    # "039": "/Users/ernie/Downloads/Tete_photos_fixed_names/19680501_185900.jpg",
    # "040": "/Users/ernie/Downloads/Tete_photos_fixed_names/19700101_224000.jpg",
    # "041": "/Users/ernie/Downloads/Tete_photos_fixed_names/19700101_224144.jpg",
    # "042": "/Users/ernie/Downloads/Tete_photos_fixed_names/19700601_191900.jpg",
    # "043": "/Users/ernie/Downloads/Tete_photos_fixed_names/19700601_191926.jpg",
    # "044": "/Users/ernie/Downloads/Tete_photos_fixed_names/19700601_192542.jpg",
    # "045": "/Users/ernie/Downloads/Tete_photos_fixed_names/19701201_181400.jpg",
    # "046": "/Users/ernie/Downloads/Tete_photos_fixed_names/19701201_181420.jpg",
    # "047": "/Users/ernie/Downloads/Tete_photos_fixed_names/19701201_182110.jpg",
    # "048": "/Users/ernie/Downloads/Tete_photos_fixed_names/19710401_182900.jpg",
    # "049": "/Users/ernie/Downloads/Tete_photos_fixed_names/19710401_182901.jpg",
    # "050": "/Users/ernie/Downloads/Tete_photos_fixed_names/19710801_190500.jpg",
    # "051": "/Users/ernie/Downloads/Tete_photos_fixed_names/19710801_194400.jpg",
    # "052": "/Users/ernie/Downloads/Tete_photos_fixed_names/19711201_184200.jpg",
    # "053": "/Users/ernie/Downloads/Tete_photos_fixed_names/19711201_184250.jpg",
    # "054": "/Users/ernie/Downloads/Tete_photos_fixed_names/19720301_184900.jpg",
    # "055": "/Users/ernie/Downloads/Tete_photos_fixed_names/19720301_185338.jpg",
    # "056": "/Users/ernie/Downloads/Tete_photos_fixed_names/19720301_185732.jpg",
    # "057": "/Users/ernie/Downloads/Tete_photos_fixed_names/19720301_185750.jpg",
    # "058": "/Users/ernie/Downloads/Tete_photos_fixed_names/19721201_182900.jpg",
    # "059": "/Users/ernie/Downloads/Tete_photos_fixed_names/19721201_182946.jpg",
    # "060": "/Users/ernie/Downloads/Tete_photos_fixed_names/19730301_230900.jpg",
    # "061": "/Users/ernie/Downloads/Tete_photos_fixed_names/19730701_201000.jpg",
    # "062": "/Users/ernie/Downloads/Tete_photos_fixed_names/19730701_201032.jpg",
    # "063": "/Users/ernie/Downloads/Tete_photos_fixed_names/19730703_192800.jpg",
    # "064": "/Users/ernie/Downloads/Tete_photos_fixed_names/19730801_200900.jpg",
    # "065": "/Users/ernie/Downloads/Tete_photos_fixed_names/19731201_183700.jpg",
    # "066": "/Users/ernie/Downloads/Tete_photos_fixed_names/19731201_190600.jpg",
    # "067": "/Users/ernie/Downloads/Tete_photos_fixed_names/19731201_190852.jpg",
    # "068": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740301_184700.jpg",
    # "069": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740301_191754.jpg",
    # "070": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740301_191912.jpg",
    # "071": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740301_191936.jpg",
    # "072": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_192300.jpg",
    # "073": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_192856.jpg",
    # "074": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_193226.jpg",
    # "075": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_193234.jpg",
    # "076": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_193320.jpg",
    # "077": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_193912.jpg",
    # "078": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_194356.jpg",
    # "079": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_195324.jpg",
    # "080": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_195550.jpg",
    # "081": "/Users/ernie/Downloads/Tete_photos_fixed_names/19740401_235400.jpg",
    # "082": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770201_200800.jpg",
    # "083": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770201_200822.jpg",
    # "084": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770201_200834.jpg",
    # "085": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770201_201000.jpg",
    # "086": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770201_201038.jpg",
    # "087": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770201_201054.jpg",
    # "088": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770202_230115.jpg",
    # "089": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770202_230316.jpg",
    # "090": "/Users/ernie/Downloads/Tete_photos_fixed_names/19770801_205700.jpg",
    # "091": "/Users/ernie/Downloads/Tete_photos_fixed_names/19771101_200700.jpg",
    # "092": "/Users/ernie/Downloads/Tete_photos_fixed_names/19780102_230838.jpg",
    # "093": "/Users/ernie/Downloads/Tete_photos_fixed_names/19780103_000704.jpg",
    # "094": "/Users/ernie/Downloads/Tete_photos_fixed_names/19790602_060000.jpg",
    # "095": "/Users/ernie/Downloads/Tete_photos_fixed_names/19800222_143041.jpg",
    # "096": "/Users/ernie/Downloads/Tete_photos_fixed_names/19811231_190000.jpg",
    # "097": "/Users/ernie/Downloads/Tete_photos_fixed_names/19820301_050000.jpg",
    # "098": "/Users/ernie/Downloads/Tete_photos_fixed_names/19821227_113900.jpg",
    # "099": "/Users/ernie/Downloads/Tete_photos_fixed_names/19831231_190000.jpg",
    # "100": "/Users/ernie/Downloads/Tete_photos_fixed_names/19860314_190000.jpg",
    # "101": "/Users/ernie/Downloads/Tete_photos_fixed_names/19860323_113500.jpg",
    # "102": "/Users/ernie/Downloads/Tete_photos_fixed_names/19900801_152000.jpg",
    # "103": "/Users/ernie/Downloads/Tete_photos_fixed_names/19911114_193500.jpg",
    # "104": "/Users/ernie/Downloads/Tete_photos_fixed_names/20011030_191517.JPG",
    # "105": "/Users/ernie/Downloads/Tete_photos_fixed_names/20030712_214955.JPG",
    # "106": "/Users/ernie/Downloads/Tete_photos_fixed_names/20030719_132421.JPG",
    # "107": "/Users/ernie/Downloads/Tete_photos_fixed_names/20030721_222750.JPG",
    # "108": "/Users/ernie/Downloads/Tete_photos_fixed_names/20030727_190137.jpg",
    # "109": "/Users/ernie/Downloads/Tete_photos_fixed_names/20030809_103457.JPG",
    # "110": "/Users/ernie/Downloads/Tete_photos_fixed_names/20030809_170717.JPG",
    # "111": "/Users/ernie/Downloads/Tete_photos_fixed_names/20031211_170214.jpg",
    # "112": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040101_102844.jpg",
    # "113": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040417_091929.JPG",
    # "114": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040418_171243.JPG",
    # "115": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040530_070125.JPG",
    # "116": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040609_085448.JPG",
    # "117": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040612_212032.JPG",
    # "118": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040710_144137.jpg",
    # "119": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040725_142309.JPG",
    # "120": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040725_174350.jpg",
    # "121": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040729_194005.jpg",
    # "122": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040804_180144.jpg",
    # "123": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040805_193813.jpg",
    # "124": "/Users/ernie/Downloads/Tete_photos_fixed_names/20040807_195835.JPG",
    # "125": "/Users/ernie/Downloads/Tete_photos_fixed_names/20041222_155359.JPG",
    # "126": "/Users/ernie/Downloads/Tete_photos_fixed_names/20050713_134549.jpg",
    # "127": "/Users/ernie/Downloads/Tete_photos_fixed_names/20050720_214726.jpg",
    # "128": "/Users/ernie/Downloads/Tete_photos_fixed_names/20050826_201336.jpg",
    # "129": "/Users/ernie/Downloads/Tete_photos_fixed_names/20050903_170613.jpg",
    # "130": "/Users/ernie/Downloads/Tete_photos_fixed_names/20051225_110552.jpg",
    # "131": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060108_112342.jpg",
    # "132": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060115_085328.jpg",
    # "133": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060115_130425.jpg",
    # "134": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060122_080033.jpg",
    # "135": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060130_130530.jpg",
    # "136": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060422_112122.JPG",
    # "137": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060422_112706.JPG",
    # "138": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060729_114404.jpg",
    # "139": "/Users/ernie/Downloads/Tete_photos_fixed_names/20060730_150055.jpg",
    # "140": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061015_054809.JPG",
    # "141": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061015_145001.JPG",
    # "142": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061105_165512.JPG",
    # "143": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061110_162100.JPG",
    # "144": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061110_234402.JPG",
    # "145": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061111_064331.jpg",
    # "146": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061111_084609.JPG",
    # "147": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061111_095652.JPG",
    # "148": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061111_110505.JPG",
    # "149": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061111_114458.JPG",
    # "150": "/Users/ernie/Downloads/Tete_photos_fixed_names/20061112_152243.jpg",
    # "151": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070217_135632.jpg",
    # "152": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070217_150716.jpg",
    # "153": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070217_174514.jpg",
    # "154": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070217_174530.jpg",
    # "155": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070224_101239.jpg",
    # "156": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070419_041540.jpg",
    # "157": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070420_162450.jpg",
    # "158": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070420_164529.jpg",
    # "159": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070421_105618.jpg",
    # "160": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070422_103226.jpg",
    # "161": "/Users/ernie/Downloads/Tete_photos_fixed_names/20070809_130537.JPG",
    # "162": "/Users/ernie/Downloads/Tete_photos_fixed_names/20071229_185937.JPG",
    # "163": "/Users/ernie/Downloads/Tete_photos_fixed_names/20071229_193946.JPG",
    # "164": "/Users/ernie/Downloads/Tete_photos_fixed_names/20080520_181149.jpg",
    # "165": "/Users/ernie/Downloads/Tete_photos_fixed_names/20080520_184103.jpg",
    # "166": "/Users/ernie/Downloads/Tete_photos_fixed_names/20081221_234828.JPG",
    # "167": "/Users/ernie/Downloads/Tete_photos_fixed_names/20081225_085958.JPG",
    # "168": "/Users/ernie/Downloads/Tete_photos_fixed_names/20090108_131840.JPG",
    # "169": "/Users/ernie/Downloads/Tete_photos_fixed_names/20090613_090023.JPG",
    # "170": "/Users/ernie/Downloads/Tete_photos_fixed_names/20090613_104307.JPG",
    # "171": "/Users/ernie/Downloads/Tete_photos_fixed_names/20090618_085700.JPG",
    # "172": "/Users/ernie/Downloads/Tete_photos_fixed_names/20091023_120615.JPG",
    # "173": "/Users/ernie/Downloads/Tete_photos_fixed_names/20091023_124146.JPG",
    # "174": "/Users/ernie/Downloads/Tete_photos_fixed_names/20100102_133036.jpg",
    # "175": "/Users/ernie/Downloads/Tete_photos_fixed_names/20110513_080628.JPG",
    # "176": "/Users/ernie/Downloads/Tete_photos_fixed_names/20120328_091337.JPG",
    # "177": "/Users/ernie/Downloads/Tete_photos_fixed_names/20120704_105126.jpg",
    # "178": "/Users/ernie/Downloads/Tete_photos_fixed_names/20120717_213715.jpg",
    # "179": "/Users/ernie/Downloads/Tete_photos_fixed_names/20120729_145946.jpg",
    # "180": "/Users/ernie/Downloads/Tete_photos_fixed_names/20120819_081622.jpg",
    # "181": "/Users/ernie/Downloads/Tete_photos_fixed_names/20120825_022027.jpg",
    # "182": "/Users/ernie/Downloads/Tete_photos_fixed_names/20121227_174351.jpg",
    # "183": "/Users/ernie/Downloads/Tete_photos_fixed_names/20121231_202206.jpg",
    # "184": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130102_105357.jpg",
    # "185": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130207_115850.jpg",
    # "186": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130606_161241.jpg",
    # "187": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130621_180948.jpg",
    # "188": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130704_185324.jpg",
    # "189": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130722_183259.jpg",
    # "190": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130907_115244.jpg",
    # "191": "/Users/ernie/Downloads/Tete_photos_fixed_names/20130925_170946.jpg",
    # "192": "/Users/ernie/Downloads/Tete_photos_fixed_names/20131011_213224.jpg",
    # "193": "/Users/ernie/Downloads/Tete_photos_fixed_names/20131013_221645.jpg",
    # "194": "/Users/ernie/Downloads/Tete_photos_fixed_names/20131222_114644.jpg",
    # "195": "/Users/ernie/Downloads/Tete_photos_fixed_names/20140210_122048.jpg",
    # "196": "/Users/ernie/Downloads/Tete_photos_fixed_names/20140210_122509.jpg",
    # "197": "/Users/ernie/Downloads/Tete_photos_fixed_names/20160922_194138.jpg",
    # "198": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161114_162417.jpg",
    # "199": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161130_213959.jpg",
    # "200": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161206_152828.jpg",
    # "201": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161206_155321.jpg",
    # "202": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161213_191020.jpg",
    # "203": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161214_093429.jpg",
    # "204": "/Users/ernie/Downloads/Tete_photos_fixed_names/20161226_164959.jpg",
    # "205": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170114_183609.jpg",
    # "206": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170114_192044.jpg",
    # "207": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170715_132210.jpg",
    # "208": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170715_153238.jpg",
    # "209": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170715_222934.JPG",
    # "210": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170715_224727.JPG",
    # "211": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170715_231522.JPG",
    # "212": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170715_234420.JPG",
    # "213": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170716_004212.JPG",
    # "214": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170716_004952.JPG",
    # "215": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170716_012540.JPG",
    # "216": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170716_223300.jpg",
    # "217": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170718_120200.jpg",
    # "218": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170827_174716.jpg",
    # "219": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170827_181029.jpg",
    # "220": "/Users/ernie/Downloads/Tete_photos_fixed_names/20170829_194505.jpg",
    # "221": "/Users/ernie/Downloads/Tete_photos_fixed_names/20171231_203105.jpg",
    # "222": "/Users/ernie/Downloads/Tete_photos_fixed_names/20181115_223940.jpg",
    # "223": "/Users/ernie/Downloads/Tete_photos_fixed_names/20181201_193408.jpg",
    # "224": "/Users/ernie/Downloads/Tete_photos_fixed_names/20181223_130513.jpg",
    # "225": "/Users/ernie/Downloads/Tete_photos_fixed_names/20181224_204047.JPG",
    # "226": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190126_112642.jpg",
    # "227": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190130_114032.jpg",
    # "228": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190215_084219.jpg",
    # "229": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190304_183739.jpg",
    # "230": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190310_225827.jpg",
    # "231": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190505_114903.jpg",
    # "232": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190629_170517.jpg",
    # "233": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190629_170844.jpg",
    # "234": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190705_140603.jpg",
    # "235": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190705_180000.jpg",
    # "236": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190705_180001.jpg",
    # "237": "/Users/ernie/Downloads/Tete_photos_fixed_names/20190705_180002.jpg",
    # "238": "/Users/ernie/Downloads/Tete_photos_fixed_names/20200411_145305.jpg",
    # "239": "/Users/ernie/Downloads/Tete_photos_fixed_names/20210327_152406.jpg",
    # "240": "/Users/ernie/Downloads/Tete_photos_fixed_names/20210906_102801.jpg",
    # "241": "/Users/ernie/Downloads/Tete_photos_fixed_names/20220509_150927.jpg",
    # "242": "/Users/ernie/Downloads/Tete_photos_fixed_names/20230306_211658.HEIC",
    # "243": "/Users/ernie/Downloads/Tete_photos_fixed_names/20230506_213451.HEIC",
    # "244": "/Users/ernie/Downloads/Tete_photos_fixed_names/20240801_054307.jpg",
}