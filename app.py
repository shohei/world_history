import streamlit as st
import pydeck as pdk
import random
import time

from features import FEATURES

# ---------------------------------------------------------------------------
# データ定義（全イベントに座標・ソート用年を付与）
# ---------------------------------------------------------------------------

ERAS = [
    {
        "name": "古代文明（～紀元前500年）",
        "color": "#8B4513",
        "events": [
            {"year": "紀元前3000年頃", "sort_year": -3000, "title": "メソポタミア文明の興隆", "detail": "チグリス川・ユーフラテス川流域でシュメール人が都市国家を建設。楔形文字を発明し、世界最古の文明の一つを築いた。", "region": "中東", "lat": 31.0, "lon": 47.0},
            {"year": "紀元前2600年頃", "sort_year": -2600, "title": "エジプト・ピラミッドの建設", "detail": "クフ王のギザの大ピラミッドが建設された。高さ約146mの巨大建造物で、古代エジプト文明の技術力を示す。", "region": "アフリカ", "lat": 29.98, "lon": 31.13},
            {"year": "紀元前1750年頃", "sort_year": -1750, "title": "ハンムラビ法典の制定", "detail": "バビロニア王ハンムラビが282条の法典を制定。「目には目を、歯には歯を」の同害報復法で知られる。", "region": "中東", "lat": 32.5, "lon": 44.4},
            {"year": "紀元前1600年頃", "sort_year": -1600, "title": "殷（商）王朝の成立", "detail": "中国最古の王朝の一つ。甲骨文字を使用し、青銅器文化が栄えた。", "region": "アジア", "lat": 36.1, "lon": 114.3},
            {"year": "紀元前1200年頃", "sort_year": -1200, "title": "トロイア戦争", "detail": "ギリシャ連合軍とトロイアの間で起きたとされる伝説的な戦争。ホメロスの叙事詩『イリアス』の題材となった。", "region": "ヨーロッパ", "lat": 39.95, "lon": 26.24},
            {"year": "紀元前776年", "sort_year": -776, "title": "古代オリンピックの開始", "detail": "古代ギリシャのオリンピアで第1回オリンピック競技祭が開催された。4年に一度、ゼウス神に捧げる祭典として行われた。", "region": "ヨーロッパ", "lat": 37.64, "lon": 21.63},
            {"year": "紀元前563年頃", "sort_year": -563, "title": "仏陀（ゴータマ・シッダールタ）の誕生", "detail": "ネパールのルンビニーで生まれ、苦行と瞑想の末に悟りを開き、仏教を創始した。", "region": "アジア", "lat": 27.47, "lon": 83.28},
        ],
    },
    {
        "name": "古典期（紀元前500年～紀元後500年）",
        "color": "#1E90FF",
        "events": [
            {"year": "紀元前490年", "sort_year": -490, "title": "マラトンの戦い", "detail": "ペルシア戦争の一戦。アテナイ軍がペルシア軍を撃退。伝令フィディピデスがアテナイまで約40km走ったという伝説がマラソン競技の起源。", "region": "ヨーロッパ", "lat": 38.12, "lon": 23.97},
            {"year": "紀元前334年", "sort_year": -334, "title": "アレクサンドロス大王の東征", "detail": "マケドニア王アレクサンドロス3世がペルシア帝国を征服し、エジプトからインドに至る大帝国を築いた。ヘレニズム文化の拡散をもたらした。", "region": "ヨーロッパ", "lat": 40.62, "lon": 22.95},
            {"year": "紀元前221年", "sort_year": -221, "title": "秦の始皇帝による中国統一", "detail": "秦王政（始皇帝）が戦国七雄を統一。度量衡・文字・貨幣を統一し、万里の長城の建設を開始した。", "region": "アジア", "lat": 34.27, "lon": 108.9},
            {"year": "紀元前44年", "sort_year": -44, "title": "カエサルの暗殺", "detail": "ローマの独裁官ユリウス・カエサルが元老院議員らに暗殺された。共和政ローマの終焉と帝政への移行の契機となった。", "region": "ヨーロッパ", "lat": 41.9, "lon": 12.5},
            {"year": "紀元前4年頃", "sort_year": -4, "title": "イエス・キリストの誕生", "detail": "ユダヤのベツレヘムで誕生したとされる。その教えは後にキリスト教として世界最大の宗教に発展した。", "region": "中東", "lat": 31.7, "lon": 35.2},
            {"year": "220年", "sort_year": 220, "title": "三国時代の始まり", "detail": "後漢の滅亡後、魏・呉・蜀の三国が鼎立。『三国志演義』の舞台としても有名。", "region": "アジア", "lat": 34.8, "lon": 113.7},
            {"year": "313年", "sort_year": 313, "title": "ミラノ勅令", "detail": "ローマ皇帝コンスタンティヌス1世がキリスト教を公認。ローマ帝国でのキリスト教の急速な拡大につながった。", "region": "ヨーロッパ", "lat": 45.46, "lon": 9.19},
            {"year": "476年", "sort_year": 476, "title": "西ローマ帝国の滅亡", "detail": "ゲルマン人傭兵隊長オドアケルが最後の西ローマ皇帝を廃位。古代ローマの終焉と中世ヨーロッパの幕開けを告げた。", "region": "ヨーロッパ", "lat": 41.9, "lon": 12.5},
        ],
    },
    {
        "name": "中世（500年～1500年）",
        "color": "#228B22",
        "events": [
            {"year": "570年頃", "sort_year": 570, "title": "ムハンマドの誕生", "detail": "メッカで誕生。610年頃に啓示を受け、イスラム教を創始。アラビア半島を統一し、イスラム文明の基礎を築いた。", "region": "中東", "lat": 21.42, "lon": 39.83},
            {"year": "710年", "sort_year": 710, "title": "奈良時代の始まり（平城京遷都）", "detail": "日本で元明天皇が平城京に遷都。律令国家の整備が進み、『古事記』『日本書紀』が編纂された。", "region": "アジア", "lat": 34.69, "lon": 135.8},
            {"year": "800年", "sort_year": 800, "title": "カール大帝の戴冠", "detail": "フランク王カールがローマ教皇レオ3世から西ローマ皇帝の冠を受けた。西ヨーロッパの政治的統一の象徴。", "region": "ヨーロッパ", "lat": 50.77, "lon": 6.08},
            {"year": "1066年", "sort_year": 1066, "title": "ノルマン・コンクエスト", "detail": "ノルマンディー公ウィリアムがイングランドを征服。ヘイスティングズの戦いでイングランド王ハロルドを破り、イングランド王となった。", "region": "ヨーロッパ", "lat": 50.91, "lon": 0.59},
            {"year": "1096年", "sort_year": 1096, "title": "第1回十字軍", "detail": "教皇ウルバヌス2世の呼びかけにより、キリスト教徒の軍がエルサレム奪還のために出征。東西文化の交流に大きな影響を与えた。", "region": "ヨーロッパ", "lat": 31.78, "lon": 35.23},
            {"year": "1206年", "sort_year": 1206, "title": "モンゴル帝国の建国", "detail": "チンギス・カンがモンゴル諸部族を統一し、モンゴル帝国を建国。史上最大の陸上帝国へと発展した。", "region": "アジア", "lat": 47.92, "lon": 106.9},
            {"year": "1347年", "sort_year": 1347, "title": "黒死病（ペスト）の大流行", "detail": "ヨーロッパ全土でペストが猛威を振るい、人口の約3分の1が死亡。社会構造の大変革をもたらした。", "region": "ヨーロッパ", "lat": 45.44, "lon": 12.32},
            {"year": "1453年", "sort_year": 1453, "title": "コンスタンティノープルの陥落", "detail": "オスマン帝国のメフメト2世がビザンツ帝国の首都コンスタンティノープルを征服。1000年以上続いた東ローマ帝国が滅亡した。", "region": "中東", "lat": 41.01, "lon": 28.98},
        ],
    },
    {
        "name": "近世（1500年～1800年）",
        "color": "#FF8C00",
        "events": [
            {"year": "1492年", "sort_year": 1492, "title": "コロンブスの新大陸到達", "detail": "スペイン女王イサベルの支援を受けたコロンブスがカリブ海の島に到達。大航海時代の幕開けとなった。", "region": "アメリカ", "lat": 24.0, "lon": -74.5},
            {"year": "1517年", "sort_year": 1517, "title": "宗教改革の開始", "detail": "マルティン・ルターが95か条の論題をヴィッテンベルク城教会の扉に掲示。カトリック教会に対する宗教改革運動が始まった。", "region": "ヨーロッパ", "lat": 51.87, "lon": 12.64},
            {"year": "1543年", "sort_year": 1543, "title": "コペルニクスの地動説", "detail": "ニコラウス・コペルニクスが『天球の回転について』を出版。地球が太陽の周りを回るという地動説を提唱し、科学革命の端緒となった。", "region": "ヨーロッパ", "lat": 53.77, "lon": 20.47},
            {"year": "1600年", "sort_year": 1600, "title": "関ヶ原の戦い", "detail": "徳川家康が石田三成を破り、天下の覇権を握った。江戸幕府成立への決定的な戦いとなった。", "region": "アジア", "lat": 35.37, "lon": 136.46},
            {"year": "1687年", "sort_year": 1687, "title": "ニュートンの『プリンキピア』", "detail": "アイザック・ニュートンが万有引力の法則を含む『自然哲学の数学的原理』を出版。近代物理学の基礎を築いた。", "region": "ヨーロッパ", "lat": 51.51, "lon": -0.13},
            {"year": "1776年", "sort_year": 1776, "title": "アメリカ独立宣言", "detail": "13植民地がイギリスからの独立を宣言。トマス・ジェファソンが起草した宣言は、自由と平等の理念を高らかに謳った。", "region": "アメリカ", "lat": 39.95, "lon": -75.15},
            {"year": "1789年", "sort_year": 1789, "title": "フランス革命", "detail": "バスティーユ牢獄の襲撃に始まるフランス革命が勃発。絶対王政が打倒され、「自由・平等・博愛」の理念が広まった。", "region": "ヨーロッパ", "lat": 48.85, "lon": 2.35},
        ],
    },
    {
        "name": "近代（1800年～1945年）",
        "color": "#DC143C",
        "events": [
            {"year": "1804年", "sort_year": 1804, "title": "ナポレオンの皇帝即位", "detail": "ナポレオン・ボナパルトがフランス皇帝に即位。ナポレオン法典を制定し、ヨーロッパ各地に近代的な法制度をもたらした。", "region": "ヨーロッパ", "lat": 48.85, "lon": 2.35},
            {"year": "1839年", "sort_year": 1839, "title": "アヘン戦争", "detail": "清国とイギリスの間で勃発。清の敗北により南京条約が結ばれ、香港がイギリスに割譲された。", "region": "アジア", "lat": 23.13, "lon": 113.26},
            {"year": "1861年", "sort_year": 1861, "title": "アメリカ南北戦争", "detail": "奴隷制をめぐり北部と南部が対立。リンカーン大統領の指導下、北軍が勝利し、奴隷制が廃止された。", "region": "アメリカ", "lat": 38.91, "lon": -77.04},
            {"year": "1868年", "sort_year": 1868, "title": "明治維新", "detail": "日本で幕藩体制が崩壊し、天皇を中心とする新政府が樹立。急速な近代化・西洋化が推進された。", "region": "アジア", "lat": 35.02, "lon": 135.76},
            {"year": "1914年", "sort_year": 1914, "title": "第一次世界大戦の開戦", "detail": "サラエボでのオーストリア皇太子暗殺を契機に勃発。同盟国と連合国が4年にわたり戦い、約1700万人が犠牲となった。", "region": "ヨーロッパ", "lat": 43.86, "lon": 18.41},
            {"year": "1917年", "sort_year": 1917, "title": "ロシア革命", "detail": "レーニン率いるボルシェヴィキが権力を掌握。世界初の社会主義国家ソビエト連邦が誕生した。", "region": "ヨーロッパ", "lat": 59.93, "lon": 30.32},
            {"year": "1929年", "sort_year": 1929, "title": "世界恐慌", "detail": "ニューヨーク株式市場の暴落をきっかけに世界的な経済危機が発生。大量失業と社会不安をもたらした。", "region": "アメリカ", "lat": 40.71, "lon": -74.01},
            {"year": "1939年", "sort_year": 1939, "title": "第二次世界大戦の開戦", "detail": "ナチス・ドイツのポーランド侵攻により勃発。6年間にわたる人類史上最大の戦争で、約6000万人が犠牲となった。", "region": "ヨーロッパ", "lat": 52.23, "lon": 21.01},
            {"year": "1945年", "sort_year": 1945, "title": "広島・長崎への原爆投下", "detail": "人類史上初の核兵器が使用された。この悲劇は核兵器廃絶と平和への願いの原点となっている。", "region": "アジア", "lat": 34.39, "lon": 132.45},
        ],
    },
    {
        "name": "現代（1945年～現在）",
        "color": "#9932CC",
        "events": [
            {"year": "1945年", "sort_year": 1945, "title": "国際連合の設立", "detail": "第二次世界大戦の反省から、国際平和と安全の維持を目的とする国際連合が設立された。本部はニューヨーク。", "region": "アメリカ", "lat": 40.75, "lon": -73.97},
            {"year": "1947年", "sort_year": 1947, "title": "インドの独立", "detail": "マハトマ・ガンディーらの非暴力抵抗運動が実り、インドがイギリスから独立。同時にパキスタンが分離独立した。", "region": "アジア", "lat": 28.61, "lon": 77.21},
            {"year": "1949年", "sort_year": 1949, "title": "中華人民共和国の成立", "detail": "毛沢東が天安門広場で建国を宣言。中国共産党による統治が始まった。", "region": "アジア", "lat": 39.91, "lon": 116.39},
            {"year": "1961年", "sort_year": 1961, "title": "ベルリンの壁建設", "detail": "東ドイツが西ベルリンを囲む壁を建設。冷戦における東西分断の象徴となった。", "region": "ヨーロッパ", "lat": 52.52, "lon": 13.41},
            {"year": "1969年", "sort_year": 1969, "title": "アポロ11号の月面着陸", "detail": "ニール・アームストロングが人類初の月面歩行を達成。「一人の人間にとっては小さな一歩だが、人類にとっては偉大な飛躍だ」", "region": "アメリカ", "lat": 28.57, "lon": -80.65},
            {"year": "1989年", "sort_year": 1989, "title": "ベルリンの壁崩壊", "detail": "東西ドイツを隔てていたベルリンの壁が崩壊。冷戦の終結を象徴する歴史的出来事となった。", "region": "ヨーロッパ", "lat": 52.52, "lon": 13.41},
            {"year": "1991年", "sort_year": 1991, "title": "ソビエト連邦の崩壊", "detail": "ゴルバチョフのペレストロイカの末、ソビエト連邦が解体。冷戦が正式に終結し、世界秩序が大きく変化した。", "region": "ヨーロッパ", "lat": 55.76, "lon": 37.62},
            {"year": "2001年", "sort_year": 2001, "title": "アメリカ同時多発テロ事件", "detail": "9月11日、ハイジャックされた旅客機がニューヨークの世界貿易センタービルなどに突入。国際テロとの戦いの契機となった。", "region": "アメリカ", "lat": 40.71, "lon": -74.01},
        ],
    },
]

ALL_EVENTS_SORTED = sorted(
    [ev for era in ERAS for ev in era["events"]],
    key=lambda e: e["sort_year"],
)

TIMELINE_STEPS = [ev["sort_year"] for ev in ALL_EVENTS_SORTED]

QUIZ_DATA = [
    {"q": "世界最古の文明の一つとされるメソポタミア文明が栄えた地域はどこ？", "choices": ["ナイル川流域", "チグリス川・ユーフラテス川流域", "インダス川流域", "黄河流域"], "answer": 1},
    {"q": "ギザの大ピラミッドを建設させたとされるファラオは誰？", "choices": ["ツタンカーメン", "ラムセス2世", "クフ王", "ハトシェプスト"], "answer": 2},
    {"q": "「目には目を、歯には歯を」で有名な法典は？", "choices": ["ローマ法大全", "ハンムラビ法典", "十二表法", "マヌ法典"], "answer": 1},
    {"q": "アレクサンドロス大王はどの国の王だった？", "choices": ["ペルシア", "エジプト", "マケドニア", "スパルタ"], "answer": 2},
    {"q": "中国を初めて統一した始皇帝は何という国の王？", "choices": ["漢", "秦", "殷", "周"], "answer": 1},
    {"q": "西ローマ帝国が滅亡した年は？", "choices": ["395年", "410年", "455年", "476年"], "answer": 3},
    {"q": "イスラム教の創始者は誰？", "choices": ["イエス", "モーセ", "ムハンマド", "仏陀"], "answer": 2},
    {"q": "モンゴル帝国を建国したのは誰？", "choices": ["フビライ・ハン", "チンギス・カン", "オゴデイ・ハン", "ティムール"], "answer": 1},
    {"q": "1492年にアメリカ大陸に到達したのは誰？", "choices": ["マゼラン", "バスコ・ダ・ガマ", "コロンブス", "ドレーク"], "answer": 2},
    {"q": "宗教改革を始めた人物は？", "choices": ["カルヴァン", "マルティン・ルター", "ヘンリー8世", "ツヴィングリ"], "answer": 1},
    {"q": "フランス革命が始まった年は？", "choices": ["1776年", "1789年", "1804年", "1815年"], "answer": 1},
    {"q": "万有引力の法則を発見した科学者は？", "choices": ["ガリレオ", "コペルニクス", "ケプラー", "ニュートン"], "answer": 3},
    {"q": "アメリカ独立宣言を起草した中心人物は？", "choices": ["ジョージ・ワシントン", "ベンジャミン・フランクリン", "トマス・ジェファソン", "ジョン・アダムズ"], "answer": 2},
    {"q": "明治維新が起きた年は？", "choices": ["1853年", "1868年", "1871年", "1889年"], "answer": 1},
    {"q": "第一次世界大戦の直接的な引き金となった事件は？", "choices": ["日露戦争", "サラエボ事件", "モロッコ事件", "ボーア戦争"], "answer": 1},
    {"q": "ロシア革命を主導した人物は？", "choices": ["スターリン", "トロツキー", "レーニン", "ケレンスキー"], "answer": 2},
    {"q": "ベルリンの壁が崩壊した年は？", "choices": ["1985年", "1989年", "1991年", "1993年"], "answer": 1},
    {"q": "インド独立運動を非暴力で指導した人物は？", "choices": ["ネルー", "ガンディー", "ジンナー", "ボース"], "answer": 1},
    {"q": "人類初の月面着陸を達成した宇宙飛行士は？", "choices": ["ニール・アームストロング", "バズ・オルドリン", "ユーリ・ガガーリン", "ジョン・グレン"], "answer": 0},
    {"q": "冷戦の終結を象徴する1991年の出来事は？", "choices": ["天安門事件", "湾岸戦争", "ソビエト連邦の崩壊", "マーストリヒト条約"], "answer": 2},
]

PERSONS = [
    {"name": "アレクサンドロス大王", "era": "古典期", "years": "紀元前356年～紀元前323年", "desc": "マケドニア王。東方遠征でペルシア帝国を征服し、エジプトからインドに至る大帝国を建設。ヘレニズム文化の創出に貢献。", "achievement": "史上最大規模の帝国を短期間で築き、東西文化の融合を促進"},
    {"name": "秦の始皇帝", "era": "古典期", "years": "紀元前259年～紀元前210年", "desc": "中国を初めて統一した皇帝。度量衡・文字・貨幣を統一し、万里の長城の建設を推進。兵馬俑でも知られる。", "achievement": "中国統一と中央集権体制の確立"},
    {"name": "ユリウス・カエサル", "era": "古典期", "years": "紀元前100年～紀元前44年", "desc": "ローマの軍人・政治家。ガリア遠征で名声を得た後、独裁官に就任。共和政から帝政への転換点を作った。", "achievement": "ローマの領土拡大とユリウス暦の制定"},
    {"name": "ムハンマド", "era": "中世", "years": "570年頃～632年", "desc": "イスラム教の創始者。メッカで啓示を受け、アラビア半島の統一を達成。イスラム文明の礎を築いた。", "achievement": "イスラム教の創始とアラビア半島の統一"},
    {"name": "チンギス・カン", "era": "中世", "years": "1162年頃～1227年", "desc": "モンゴル帝国の建国者。遊牧民を統一し、ユーラシア大陸にまたがる史上最大の陸上帝国を築いた。", "achievement": "モンゴル帝国の建国と東西交易路の整備"},
    {"name": "レオナルド・ダ・ヴィンチ", "era": "近世", "years": "1452年～1519年", "desc": "イタリアのルネサンス期を代表する万能の天才。絵画・彫刻・建築・科学・工学など多方面で優れた業績を残した。", "achievement": "『モナ・リザ』『最後の晩餐』の制作、飛行機械の設計"},
    {"name": "ナポレオン・ボナパルト", "era": "近代", "years": "1769年～1821年", "desc": "フランス革命後に権力を握りフランス皇帝に即位。ヨーロッパの大部分を支配したが、ロシア遠征の失敗後に失脚。", "achievement": "ナポレオン法典の制定とヨーロッパの近代化促進"},
    {"name": "マハトマ・ガンディー", "era": "現代", "years": "1869年～1948年", "desc": "インド独立運動の指導者。非暴力・不服従運動を展開し、イギリスからのインド独立を実現した。", "achievement": "非暴力抵抗運動によるインド独立の達成"},
]

REGION_COLORS = {
    "ヨーロッパ": "#1E90FF",
    "アジア": "#FF6347",
    "中東": "#FFD700",
    "アフリカ": "#32CD32",
    "アメリカ": "#9370DB",
}

REGION_RGB = {
    "ヨーロッパ": [30, 144, 255],
    "アジア": [255, 99, 71],
    "中東": [255, 215, 0],
    "アフリカ": [50, 205, 50],
    "アメリカ": [147, 112, 219],
}


def year_label(y: int) -> str:
    if y < 0:
        return f"紀元前{-y}年"
    return f"{y}年"


# ---------------------------------------------------------------------------
# ページ設定
# ---------------------------------------------------------------------------
st.set_page_config(page_title="世界史インタラクティブ学習", page_icon="🌍", layout="wide")

st.markdown(
    """
    <style>
    .era-header {
        padding: 10px 20px; border-radius: 8px; color: white;
        font-size: 1.3em; font-weight: bold; margin: 10px 0;
    }
    .event-card {
        background: #f8f9fa; border-left: 5px solid #1E90FF;
        padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0;
    }
    .event-year { font-weight: bold; color: #333; font-size: 1.1em; }
    .event-title { font-size: 1.2em; font-weight: bold; margin: 5px 0; }
    .person-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 20px; border-radius: 12px; margin: 10px 0;
    }
    .quiz-correct {
        background: #d4edda; border: 2px solid #28a745;
        padding: 15px; border-radius: 8px; margin: 10px 0;
    }
    .quiz-wrong {
        background: #f8d7da; border: 2px solid #dc3545;
        padding: 15px; border-radius: 8px; margin: 10px 0;
    }
    .score-display {
        font-size: 2em; font-weight: bold; text-align: center; padding: 20px;
    }
    .region-tag {
        display: inline-block; padding: 2px 10px; border-radius: 12px;
        color: white; font-size: 0.85em; font-weight: bold;
    }
    .map-event-info {
        background: #1a1a2e; color: #eee; padding: 18px;
        border-radius: 10px; margin: 6px 0; border-left: 4px solid #e94560;
    }
    .map-event-info h4 { margin: 0 0 4px 0; color: #e94560; }
    .map-event-info .year-badge {
        display: inline-block; background: #e94560; color: #fff;
        padding: 2px 10px; border-radius: 10px; font-size: 0.85em; margin-bottom: 8px;
    }
    .map-new-event {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌍 世界史インタラクティブ学習")
st.caption("時代を探索し、クイズに挑戦して、世界史の知識を深めよう！")

# ---------------------------------------------------------------------------
# タブ構成
# ---------------------------------------------------------------------------
tab_map, tab_timeline, tab_feature, tab_persons, tab_quiz, tab_compare = st.tabs(
    ["🗺️ 地図タイムライン", "📜 年表", "📚 特集", "👤 人物", "🎯 クイズ", "🔍 時代比較"]
)

# ===================== 地図タイムラインタブ =====================
with tab_map:
    st.header("🗺️ 地図タイムライン")
    st.write("スライダーで時代を動かすと、その時点までの出来事が地図上に表示されます。")

    if "map_step" not in st.session_state:
        st.session_state.map_step = len(TIMELINE_STEPS) - 1
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "play_speed" not in st.session_state:
        st.session_state.play_speed = 1.0

    max_map_step = len(TIMELINE_STEPS) - 1
    def _set_map_step(v):
        st.session_state.map_step = v
        st.session_state._map_slider_val = v

    ctrl_cols = st.columns([1, 1, 1, 1, 1, 1, 6])
    with ctrl_cols[0]:
        if st.button("⏮", use_container_width=True, key="map_first"):
            _set_map_step(0)
            st.session_state.playing = False
            st.rerun()
    with ctrl_cols[1]:
        if st.button("◀", use_container_width=True, key="map_prev"):
            st.session_state.playing = False
            if st.session_state.map_step > 0:
                _set_map_step(st.session_state.map_step - 1)
            st.rerun()
    with ctrl_cols[2]:
        play_label = "⏸" if st.session_state.playing else "▶"
        if st.button(play_label, use_container_width=True, key="map_play"):
            st.session_state.playing = not st.session_state.playing
            if st.session_state.playing and st.session_state.map_step >= max_map_step:
                _set_map_step(0)
            st.rerun()
    with ctrl_cols[3]:
        if st.button("▶", use_container_width=True, key="map_next"):
            st.session_state.playing = False
            if st.session_state.map_step < max_map_step:
                _set_map_step(st.session_state.map_step + 1)
            st.rerun()
    with ctrl_cols[4]:
        if st.button("⏭", use_container_width=True, key="map_last"):
            _set_map_step(max_map_step)
            st.session_state.playing = False
            st.rerun()
    with ctrl_cols[5]:
        speed = st.selectbox("速度", [0.5, 1.0, 1.5, 2.0], index=1, format_func=lambda x: f"×{x}", label_visibility="collapsed")
        st.session_state.play_speed = speed
    with ctrl_cols[6]:
        def _on_map_slider():
            st.session_state.map_step = st.session_state._map_slider_val
        st.slider(
            "タイムライン",
            min_value=0,
            max_value=max_map_step,
            value=st.session_state.map_step,
            format="",
            key="_map_slider_val",
            on_change=_on_map_slider,
            label_visibility="collapsed",
        )

    current_year = TIMELINE_STEPS[st.session_state.map_step]
    visible_events = [ev for ev in ALL_EVENTS_SORTED if ev["sort_year"] <= current_year]
    latest_event = ALL_EVENTS_SORTED[st.session_state.map_step]

    era_label = ""
    for era in ERAS:
        for ev in era["events"]:
            if ev is latest_event:
                era_label = era["name"]
                break

    map_data = []
    for ev in visible_events:
        is_latest = ev is latest_event
        rgb = REGION_RGB.get(ev["region"], [128, 128, 128])
        map_data.append({
            "lat": ev["lat"],
            "lon": ev["lon"],
            "title": ev["title"],
            "year": ev["year"],
            "region": ev["region"],
            "detail": ev["detail"],
            "r": rgb[0],
            "g": rgb[1],
            "b": rgb[2],
            "radius": 140000 if is_latest else 60000,
            "opacity": 240 if is_latest else 120,
        })

    view_state = pdk.ViewState(latitude=20, longitude=30, zoom=1.1, pitch=0)

    scatter = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position=["lon", "lat"],
        get_radius="radius",
        get_fill_color=["r", "g", "b", "opacity"],
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0, 100],
    )

    deck = pdk.Deck(
        layers=[scatter],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>{title}</b><br/>{year}<br/>{region}<br/>{detail}",
            "style": {
                "backgroundColor": "#1a1a2e", "color": "white",
                "fontSize": "13px", "maxWidth": "320px",
                "padding": "10px", "borderRadius": "8px",
            },
        },
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    )

    map_col, detail_col = st.columns([3, 2])
    with map_col:
        st.pydeck_chart(deck, height=380, use_container_width=True)
    with detail_col:
        st.markdown(
            f'<div class="map-event-info map-new-event" style="margin-top:0">'
            f'<span class="year-badge">{latest_event["year"]}</span> '
            f'<span class="region-tag" style="background-color: {REGION_COLORS.get(latest_event["region"], "#888")}">{latest_event["region"]}</span>'
            f'<h4>{latest_event["title"]}</h4>'
            f'<p>{latest_event["detail"]}</p>'
            f"</div>",
            unsafe_allow_html=True,
        )
        if era_label:
            st.caption(f"時代: {era_label}")
        st.markdown(f"**{st.session_state.map_step + 1} / {len(ALL_EVENTS_SORTED)} 件**")
        st.progress((st.session_state.map_step + 1) / len(ALL_EVENTS_SORTED))
        legend_html = " ".join(
            f'<span class="region-tag" style="background-color: {color}">{region}: '
            f'{sum(1 for ev in visible_events if ev["region"] == region)}件</span>'
            for region, color in REGION_COLORS.items()
        )
        st.markdown(legend_html, unsafe_allow_html=True)

    if st.session_state.playing:
        delay = 1.5 / st.session_state.play_speed
        time.sleep(delay)
        if st.session_state.map_step < len(TIMELINE_STEPS) - 1:
            _set_map_step(st.session_state.map_step + 1)
            st.rerun()
        else:
            st.session_state.playing = False
            st.rerun()

# ===================== 年表タブ =====================
with tab_timeline:
    st.header("📜 年表・タイムライン")

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_era = st.selectbox(
            "時代を選択",
            ["すべての時代"] + [e["name"] for e in ERAS],
        )
    with col_filter2:
        selected_region = st.selectbox(
            "地域で絞り込み",
            ["すべての地域", "ヨーロッパ", "アジア", "中東", "アフリカ", "アメリカ"],
        )

    for era in ERAS:
        if selected_era != "すべての時代" and era["name"] != selected_era:
            continue
        events = era["events"]
        if selected_region != "すべての地域":
            events = [e for e in events if e["region"] == selected_region]
        if not events:
            continue

        st.markdown(
            f'<div class="era-header" style="background-color: {era["color"]}">{era["name"]}</div>',
            unsafe_allow_html=True,
        )
        for event in events:
            region_color = REGION_COLORS.get(event["region"], "#888")
            with st.expander(f"**{event['year']}** — {event['title']}"):
                st.markdown(
                    f'<span class="region-tag" style="background-color: {region_color}">{event["region"]}</span>',
                    unsafe_allow_html=True,
                )
                st.write("")
                st.write(event["detail"])

# ===================== 特集タブ =====================
with tab_feature:
    st.header("📚 特集ページ")

    feature_names = list(FEATURES.keys())
    feature_labels = [f'{FEATURES[n]["icon"]} {n}' for n in feature_names]

    selected_label = st.selectbox("特集を選択", feature_labels)
    sel_idx = feature_labels.index(selected_label)
    sel_name = feature_names[sel_idx]
    feat = FEATURES[sel_name]

    st.markdown(
        f'<div class="era-header" style="background-color: {feat["color"]}">'
        f'{feat["icon"]} {sel_name}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"*{feat['summary']}*")

    feat_tab_map, feat_tab_events, feat_tab_persons = st.tabs(
        ["🗺️ 地図で見る", "📜 年表", "👤 人物"]
    )

    with feat_tab_map:
        feat_events = feat["events"]
        if "feat_step" not in st.session_state:
            st.session_state.feat_step = len(feat_events) - 1
        if "feat_playing" not in st.session_state:
            st.session_state.feat_playing = False
        if "feat_last_feature" not in st.session_state:
            st.session_state.feat_last_feature = sel_name

        if st.session_state.feat_last_feature != sel_name:
            st.session_state.feat_step = len(feat_events) - 1
            st.session_state.feat_playing = False
            st.session_state.feat_last_feature = sel_name

        max_step = len(feat_events) - 1
        if st.session_state.feat_step > max_step:
            st.session_state.feat_step = max_step

        def _set_feat_step(v):
            st.session_state.feat_step = v
            st.session_state._feat_slider_val = v

        ctrl_row = st.columns([1, 1, 1, 1, 1, 8])
        with ctrl_row[0]:
            if st.button("⏮", key="feat_first", use_container_width=True):
                _set_feat_step(0)
                st.session_state.feat_playing = False
                st.rerun()
        with ctrl_row[1]:
            if st.button("◀", key="feat_prev", use_container_width=True):
                st.session_state.feat_playing = False
                if st.session_state.feat_step > 0:
                    _set_feat_step(st.session_state.feat_step - 1)
                st.rerun()
        with ctrl_row[2]:
            fp_label = "⏸" if st.session_state.feat_playing else "▶"
            if st.button(fp_label, key="feat_play", use_container_width=True):
                st.session_state.feat_playing = not st.session_state.feat_playing
                if st.session_state.feat_playing and st.session_state.feat_step >= max_step:
                    _set_feat_step(0)
                st.rerun()
        with ctrl_row[3]:
            if st.button("▶", key="feat_next", use_container_width=True):
                st.session_state.feat_playing = False
                if st.session_state.feat_step < max_step:
                    _set_feat_step(st.session_state.feat_step + 1)
                st.rerun()
        with ctrl_row[4]:
            if st.button("⏭", key="feat_last", use_container_width=True):
                _set_feat_step(max_step)
                st.session_state.feat_playing = False
                st.rerun()
        with ctrl_row[5]:
            def _on_feat_slider():
                st.session_state.feat_step = st.session_state._feat_slider_val
            st.slider(
                "タイムライン",
                min_value=0,
                max_value=max_step,
                value=st.session_state.feat_step,
                format="",
                key="_feat_slider_val",
                on_change=_on_feat_slider,
                label_visibility="collapsed",
            )

        current_ev = feat_events[st.session_state.feat_step]
        visible_feat = feat_events[: st.session_state.feat_step + 1]

        f_map_data = []
        for ev in visible_feat:
            is_cur = ev is current_ev
            f_map_data.append({
                "lat": ev["lat"],
                "lon": ev["lon"],
                "title": ev["title"],
                "year": ev["year"],
                "detail": ev["detail"],
                "label": f'{ev["year"]}  {ev["title"]}',
                "r": 230 if is_cur else 100,
                "g": 69 if is_cur else 100,
                "b": 96 if is_cur else 180,
                "text_r": 255 if is_cur else 200,
                "text_g": 255 if is_cur else 200,
                "text_b": 255 if is_cur else 200,
                "text_a": 255 if is_cur else 160,
                "radius": 30000 if is_cur else 16000,
                "opacity": 230 if is_cur else 110,
                "font_size": 15 if is_cur else 12,
            })

        all_lats = [e["lat"] for e in feat_events]
        all_lons = [e["lon"] for e in feat_events]
        center_lat = sum(all_lats) / len(all_lats)
        center_lon = sum(all_lons) / len(all_lons)

        lat_range = max(all_lats) - min(all_lats)
        lon_range = max(all_lons) - min(all_lons)
        span = max(lat_range, lon_range)
        if span < 5:
            f_zoom = 6
        elif span < 15:
            f_zoom = 5
        elif span < 40:
            f_zoom = 4
        else:
            f_zoom = 2.5

        f_view = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=f_zoom, pitch=0)
        f_scatter = pdk.Layer(
            "ScatterplotLayer",
            data=f_map_data,
            get_position=["lon", "lat"],
            get_radius="radius",
            get_fill_color=["r", "g", "b", "opacity"],
            pickable=True,
            auto_highlight=True,
            highlight_color=[255, 255, 0, 100],
        )
        f_text = pdk.Layer(
            "TextLayer",
            data=f_map_data,
            get_position=["lon", "lat"],
            get_text="label",
            get_size="font_size",
            get_color=["text_r", "text_g", "text_b", "text_a"],
            get_angle=0,
            get_text_anchor='"start"',
            get_alignment_baseline='"center"',
            get_pixel_offset=[18, 0],
            font_family='"Hiragino Sans", "Noto Sans JP", sans-serif',
            billboard=False,
            size_scale=1,
            size_units='"pixels"',
            size_min_pixels=10,
            size_max_pixels=18,
        )
        f_deck = pdk.Deck(
            layers=[f_scatter, f_text],
            initial_view_state=f_view,
            tooltip={
                "html": "<b>{title}</b><br/>{year}<br/>{detail}",
                "style": {
                    "backgroundColor": "#1a1a2e", "color": "white",
                    "fontSize": "13px", "maxWidth": "320px",
                    "padding": "10px", "borderRadius": "8px",
                },
            },
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        )

        map_col, detail_col = st.columns([3, 2])
        with map_col:
            st.pydeck_chart(f_deck, height=380, use_container_width=True)
        with detail_col:
            st.markdown(
                f'<div class="map-event-info map-new-event" style="margin-top:0">'
                f'<span class="year-badge">{current_ev["year"]}</span>'
                f'<h4>{current_ev["title"]}</h4>'
                f'<p>{current_ev["detail"]}</p>'
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**{st.session_state.feat_step + 1} / {len(feat_events)}**")
            st.progress((st.session_state.feat_step + 1) / len(feat_events))

        if st.session_state.feat_playing:
            time.sleep(1.8)
            if st.session_state.feat_step < max_step:
                _set_feat_step(st.session_state.feat_step + 1)
                st.rerun()
            else:
                st.session_state.feat_playing = False
                st.rerun()

    with feat_tab_events:
        for ev in feat["events"]:
            with st.expander(f"**{ev['year']}** — {ev['title']}"):
                st.write(ev["detail"])

    with feat_tab_persons:
        persons = feat.get("persons", [])
        if not persons:
            st.info("この特集に人物データはありません。")
        for i in range(0, len(persons), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(persons):
                    p = persons[i + j]
                    with col:
                        st.markdown(
                            f'<div class="person-card" style="background: linear-gradient(135deg, {feat["color"]}cc 0%, {feat["color"]}88 100%)">'
                            f'<h3 style="margin:0">{p["name"]}</h3>'
                            f'<p style="opacity:0.85; margin:5px 0">{p["years"]}</p>'
                            f'<p>{p["desc"]}</p>'
                            f'<p><strong>主な功績：</strong>{p["achievement"]}</p>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )

# ===================== 人物タブ =====================
with tab_persons:
    st.header("👤 歴史上の人物")
    person_era_filter = st.selectbox(
        "時代で絞り込み",
        ["すべて", "古典期", "中世", "近世", "近代", "現代"],
        key="person_era",
    )
    filtered = PERSONS if person_era_filter == "すべて" else [p for p in PERSONS if p["era"] == person_era_filter]
    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(filtered):
                p = filtered[i + j]
                with col:
                    st.markdown(
                        f'<div class="person-card">'
                        f'<h3 style="margin:0">{p["name"]}</h3>'
                        f'<p style="opacity:0.8; margin:5px 0">{p["years"]}（{p["era"]}）</p>'
                        f'<p>{p["desc"]}</p>'
                        f'<p><strong>主な功績：</strong>{p["achievement"]}</p>'
                        f"</div>",
                        unsafe_allow_html=True,
                    )

# ===================== クイズタブ =====================
with tab_quiz:
    st.header("🎯 世界史クイズに挑戦！")

    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.quiz_questions = []
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False

    col_q1, col_q2 = st.columns([3, 1])
    with col_q1:
        num_questions = st.slider("出題数", min_value=5, max_value=len(QUIZ_DATA), value=10, step=1)
    with col_q2:
        st.write("")
        st.write("")
        if st.button("🔄 新しいクイズを開始", use_container_width=True):
            st.session_state.quiz_questions = random.sample(QUIZ_DATA, min(num_questions, len(QUIZ_DATA)))
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_started = True
            st.rerun()

    if st.session_state.quiz_started and st.session_state.quiz_questions:
        with st.form("quiz_form"):
            for idx, q in enumerate(st.session_state.quiz_questions):
                st.markdown(f"**Q{idx + 1}. {q['q']}**")
                st.session_state.quiz_answers[idx] = st.radio(
                    f"選択肢（Q{idx + 1}）",
                    options=range(len(q["choices"])),
                    format_func=lambda x, q=q: q["choices"][x],
                    key=f"q_{idx}",
                    label_visibility="collapsed",
                )
                st.divider()
            submitted = st.form_submit_button("📝 回答を提出する", use_container_width=True)
            if submitted:
                st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            correct = 0
            total = len(st.session_state.quiz_questions)
            st.subheader("📊 結果発表")
            for idx, q in enumerate(st.session_state.quiz_questions):
                user_ans = st.session_state.quiz_answers.get(idx, -1)
                is_correct = user_ans == q["answer"]
                if is_correct:
                    correct += 1
                icon = "✅" if is_correct else "❌"
                css_class = "quiz-correct" if is_correct else "quiz-wrong"
                explanation = "" if is_correct else f"<br>正解: <strong>{q['choices'][q['answer']]}</strong>"
                st.markdown(
                    f'<div class="{css_class}">{icon} Q{idx + 1}. {q["q"]}<br>'
                    f'あなたの回答: <strong>{q["choices"][user_ans]}</strong>{explanation}</div>',
                    unsafe_allow_html=True,
                )
            pct = int(correct / total * 100)
            if pct >= 80:
                grade, color = "🏆 素晴らしい！歴史博士レベル！", "#28a745"
            elif pct >= 60:
                grade, color = "👍 なかなかの知識です！", "#17a2b8"
            elif pct >= 40:
                grade, color = "📚 もう少し勉強しましょう！", "#ffc107"
            else:
                grade, color = "💪 頑張って復習しましょう！", "#dc3545"
            st.markdown(
                f'<div class="score-display" style="color: {color}">'
                f"{correct} / {total} 正解（{pct}%）<br>"
                f'<span style="font-size: 0.6em">{grade}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("「新しいクイズを開始」ボタンを押してクイズを始めましょう！")

# ===================== 時代比較タブ =====================
with tab_compare:
    st.header("🔍 時代比較")
    st.write("2つの時代を選んで、同時期に世界で何が起きていたか比較してみましょう。")
    col_a, col_b = st.columns(2)
    era_names = [e["name"] for e in ERAS]
    with col_a:
        era_a = st.selectbox("時代A", era_names, index=0, key="compare_a")
    with col_b:
        era_b = st.selectbox("時代B", era_names, index=1, key="compare_b")
    era_a_data = next(e for e in ERAS if e["name"] == era_a)
    era_b_data = next(e for e in ERAS if e["name"] == era_b)
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(
            f'<div class="era-header" style="background-color: {era_a_data["color"]}">{era_a_data["name"]}</div>',
            unsafe_allow_html=True,
        )
        for ev in era_a_data["events"]:
            region_color = REGION_COLORS.get(ev["region"], "#888")
            st.markdown(
                f'<div class="event-card" style="border-left-color: {era_a_data["color"]}">'
                f'<span class="event-year">{ev["year"]}</span> '
                f'<span class="region-tag" style="background-color: {region_color}">{ev["region"]}</span>'
                f'<div class="event-title">{ev["title"]}</div>'
                f"<p>{ev['detail']}</p></div>",
                unsafe_allow_html=True,
            )
    with col_right:
        st.markdown(
            f'<div class="era-header" style="background-color: {era_b_data["color"]}">{era_b_data["name"]}</div>',
            unsafe_allow_html=True,
        )
        for ev in era_b_data["events"]:
            region_color = REGION_COLORS.get(ev["region"], "#888")
            st.markdown(
                f'<div class="event-card" style="border-left-color: {era_b_data["color"]}">'
                f'<span class="event-year">{ev["year"]}</span> '
                f'<span class="region-tag" style="background-color: {region_color}">{ev["region"]}</span>'
                f'<div class="event-title">{ev["title"]}</div>'
                f"<p>{ev['detail']}</p></div>",
                unsafe_allow_html=True,
            )
    if era_a == era_b:
        st.warning("異なる時代を選択すると、比較がより面白くなります！")
    else:
        st.success(f"💡 **比較のポイント**: 「{era_a_data['name']}」と「{era_b_data['name']}」の出来事を見比べて、世界がどのように変化したか考えてみましょう。")

# ---------------------------------------------------------------------------
# サイドバー
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("📖 学習ガイド")
    st.markdown(
        """
        ### 使い方
        1. **🗺️ 地図** — 地図上で歴史イベントを時系列再生
        2. **📜 年表** — 時代・地域ごとに歴史的事件を閲覧
        3. **📚 特集** — テーマ別の深掘りページ
        4. **👤 人物** — 歴史上の重要人物を学習
        5. **🎯 クイズ** — 知識をテスト
        6. **🔍 比較** — 異なる時代を並べて比較

        ---
        ### 時代区分
        """
    )
    for era in ERAS:
        st.markdown(
            f'<span style="color: {era["color"]}; font-weight: bold">●</span> {era["name"]}',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 📚 特集一覧")
    for name, f in FEATURES.items():
        st.markdown(f'{f["icon"]} {name}')

    st.markdown("---")
    all_events = sum(len(e["events"]) for e in ERAS)
    feat_events_count = sum(len(f["events"]) for f in FEATURES.values())
    feat_persons_count = sum(len(f.get("persons", [])) for f in FEATURES.values())
    st.metric("収録イベント数", f"{all_events + feat_events_count} 件")
    st.metric("収録人物数", f"{len(PERSONS) + feat_persons_count} 人")
    st.metric("クイズ問題数", f"{len(QUIZ_DATA)} 問")
