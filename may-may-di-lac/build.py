import base64, html, json, pathlib

ROOT = pathlib.Path('/home/user/ai-productivity-tool/may-may-di-lac')
IMG = ROOT / 'nhan-vat'
OUT = ROOT / 'index.html'
E = html.escape

def b64(name):
    return 'data:image/webp;base64,' + base64.b64encode((IMG / name).read_bytes()).decode()

# ---------------------------------------------------------------- NHÂN VẬT
CHARS = {
    'bap': dict(name='Bé Bắp', ref='@Image1', file='bap.webp', role='Nhân vật chính · 7 tuổi',
        trait='Hiếu động, tò mò, nhanh trí. Tự nhận là "thám tử nhí", mang theo kính lúp nhựa trong cặp.',
        look='Tóc đen ngắn, mái lởm chởm; mắt nâu to; tàn nhang nhẹ; áo polo vàng 2 cúc trắng; quần short xanh navy; tất trắng; giày trắng sọc xanh dương.',
        lock='Bap (@Image1): 7-year-old Vietnamese boy, short messy black hair with spiky fringe, big glossy brown eyes, light freckles, rosy cheeks, yellow short-sleeve polo shirt with two white buttons, navy blue shorts, white socks, white sneakers with blue stripes',
        voice='Giọng bé trai trong, nhanh, hay reo lên.'),
    'na': dict(name='Bé Na', ref='@Image2', file='na.webp', role='Bạn thân của Bắp · 7 tuổi',
        trait='Vui vẻ, chu đáo, thích chăm cây. Là người đầu tiên hắt xì trong "dây chuyền hắt xì".',
        look='Tóc đen buộc 2 bím thấp dây chun hồng, mái lệch; áo thun hồng; yếm jean ngắn khóa bạc, gấu xắn; tất trắng; giày trắng-hồng.',
        lock='Na (@Image2): 7-year-old Vietnamese girl, black hair in two low pigtails with pink hair ties, side-swept bangs, big brown eyes, pink T-shirt, blue denim overall shorts with silver buckles and cuffed hems, white socks, white-and-pink sneakers',
        voice='Giọng bé gái cao, ngọt, hay cười khúc khích.'),
    'su': dict(name='Bé Su', ref='@Image3', file='su.webp', role='Bạn thân của Bắp · 6–7 tuổi',
        trait='Mũm mĩm, hiền, hay cười to. Đạp xe đến trường trong cảnh 7.',
        look='Mặt tròn, tóc đen thẳng có mái; áo thun xanh bạc hà; quần short kaki be; tất trắng; giày trắng-cam.',
        lock='Su (@Image3): chubby 6-year-old Vietnamese boy, round face, short straight black hair with bangs, big brown eyes, mint green T-shirt, beige khaki shorts, white socks, orange-and-white sneakers',
        voice='Giọng bé trai hơi trầm, chậm, dễ thương.'),
    'co': dict(name='Cô giáo', ref='@Image4', file='co-giao.webp', role='Giáo viên chủ nhiệm · ngoài 25 tuổi',
        trait='Dịu dàng, ân cần, giải thích dễ hiểu. Giữ giọng dẫn chuyện (voice-over) ở cảnh 4–6.',
        look='Tóc đen buộc đuôi ngựa thấp, vài lọn mái rơi; áo sơ mi xanh nhạt xắn tay; quần âu xanh navy ống đứng; giày búp bê màu be.',
        lock='the Teacher (@Image4): young Vietnamese female teacher in her late 20s, black hair in a low ponytail with loose strands framing the face, gentle warm smile, light blue button-up shirt with rolled sleeves, navy straight trousers, beige flat shoes',
        voice='Giọng nữ ấm, truyền cảm, tốc độ vừa.'),
    'may': dict(name='Mây Mây', ref='@Image5', file='may-may.webp', role='Đám mây con · nhân vật trung tâm',
        trait='Tinh nghịch, không nói tiếng người mà phát ra "tít tít, bíp bíp", cười khúc khích. Có 3 trạng thái: Trắng phau → Xám xịt → Phát sáng.',
        look='Đám mây bông trắng, mềm như kẹo bông; mắt nâu to có mi; lông mày cong nhỏ; má hồng; miệng nhỏ; 2 bàn tay mây nhỏ; luôn lơ lửng, có bóng mờ bên dưới.',
        lock='Mây Mây (@Image5): small fluffy white cumulus cloud character about the size of a beach ball, cotton-candy texture, big glossy brown eyes with lashes, small arched eyebrows, pink blush cheeks, tiny smiling mouth, two small soft cloud mitten hands, always floating with a soft shadow below',
        voice='SFX giọng: "tít tít, bíp bíp", tiếng cười khúc khích, tiếng ho nhỏ.'),
}
EXTRA_CHARS = [
    ('Mây Mây (xám)', 'Biến thể trạng thái của Mây Mây, cảnh 2–6.', 'Grey Mây Mây: same design as @Image5 but dirty ash-grey (#8A8D91) with black soot specks (#3F4046), droopy half-closed eyes, no blush, body slightly deflated and trembling.'),
    ('Mây Mây (phát sáng)', 'Biến thể hồi phục, cảnh 8.', 'Glowing Mây Mây: same design as @Image5, pure white with a soft golden rim light (#FFE3A3) and tiny floating sparkles.'),
    ('Tiểu yêu PM2.5', 'Nhân vật đồ họa, cảnh 4–5. Chưa có sheet, nên tạo trước khi render.', 'PM2.5 gremlin: tiny round dust-mite creature, dark purple-grey (#5B4B73), soft rubbery spikes, mismatched goofy eyes, buck-tooth grin, clumsy and silly rather than scary.'),
    ('Bố mẹ Bắp', 'Xuất hiện ở cảnh 7.2. Chưa có sheet, cần tạo cùng phong cách trước khi render.', 'Bap\'s parents: friendly Vietnamese couple in their 30s; dad with short black hair, glasses, grey T-shirt; mom with shoulder-length black hair, pale yellow blouse; same 3D style as the reference sheets.'),
]
ORDER = ['bap', 'na', 'su', 'co', 'may']

# ---------------------------------------------------------------- BẢNG MÀU KHÓA
PALETTE = [
    ('Bộ màu chính (ngày đẹp trời)', [
        ('#8FD3FF', 'Trời xanh', 'Bầu trời, nền chính'),
        ('#FFFFFF', 'Mây trắng', 'Mây Mây, đàn mây'),
        ('#E3ECF6', 'Bóng mây', 'Vùng tối trên mây'),
        ('#7CC66B', 'Cỏ sân trường', 'Bãi cỏ, cây xanh'),
        ('#F7C826', 'Vàng Bắp', 'Áo Bắp, điểm nhấn'),
        ('#FFE3A3', 'Nắng ấm', 'Ánh nắng, viền sáng'),
    ]),
    ('Màu trang phục (không đổi giữa các cảnh)', [
        ('#F4A6C6', 'Hồng Na', 'Áo Na, dây buộc tóc'),
        ('#4F74B8', 'Jean Na', 'Yếm jean'),
        ('#7FCB98', 'Bạc hà Su', 'Áo Su'),
        ('#D8C8A8', 'Kaki Su', 'Quần Su'),
        ('#A9CBEF', 'Xanh áo cô', 'Áo sơ mi cô giáo'),
        ('#1F2A55', 'Navy', 'Quần Bắp, quần cô giáo'),
    ]),
    ('Bộ màu ô nhiễm (cảnh 2–5)', [
        ('#8A8D91', 'Khói xám', 'Mây Mây xám, khói xe'),
        ('#3F4046', 'Bồ hóng', 'Chấm đen, khói đốt rác'),
        ('#A08C72', 'Bụi đất', 'Bụi công trình'),
        ('#5B4B73', 'Tím bụi mịn', 'Tiểu yêu PM2.5'),
        ('#C9B9A0', 'Trời mù', 'Bầu trời ngập khói'),
    ]),
    ('Bộ màu đồ họa (Animation in Animation)', [
        ('#2B2B3A', 'Nét viền', 'Viền dày bo tròn'),
        ('#FFF8EC', 'Giấy kem', 'Nền đồ họa'),
        ('#4CB050', 'Xanh sống xanh', 'Mầm cây, thùng rác'),
        ('#E8473C', 'Đỏ cảnh báo', 'Biển cấm đốt rác'),
        ('#3AA0E8', 'Xanh xe buýt', 'Xe buýt mặt cười'),
    ]),
]
COLOR_SCRIPT = [
    ('1', 'Sân trường nắng', '#8FD3FF', '#7CC66B', 'Tươi, bão hòa +10%'),
    ('2', 'Biến cố ngoài cổng', '#C9B9A0', '#8A8D91', 'Giảm bão hòa −40%, mù khói'),
    ('3', 'Khám bệnh', '#B9D9EE', '#8A8D91', 'Nắng dịu, Mây Mây xám nổi bật'),
    ('4', 'Nguyên nhân', '#FFF8EC', '#3F4046', 'Đồ họa giấy, khói đen'),
    ('5', 'Tác động', '#5B4B73', '#8A8D91', 'Vi mô, tối nhẹ, tím'),
    ('6', 'Sống xanh', '#FFF8EC', '#4CB050', 'Đồ họa sáng, xanh lá'),
    ('7', 'Hành động', '#8FD3FF', '#4CB050', 'Nhịp nhanh, nắng sớm'),
    ('8', 'Mây Mây khỏe lại', '#8FD3FF', '#FFE3A3', 'Viền sáng vàng, lấp lánh'),
    ('9', 'Tạm biệt', '#6EC3FA', '#FFFFFF', 'Trời cao, xanh thẳm'),
    ('10', 'Thông điệp', '#8FD3FF', '#4CB050', 'Rực rỡ, trái đất xanh'),
]
STYLE_LOCK = ('Style lock: high-end 3D animated family film, soft stylized rendering, rounded friendly shapes, '
    'subsurface-scattering skin, big glossy eyes, characters must match reference sheets exactly (same faces, hair, outfits, colors). '
    'Locked palette: sky blue #8FD3FF, cloud white #FFFFFF, grass green #7CC66B, sunny yellow #F7C826, warm sunlight #FFE3A3; '
    'soft natural daylight 5600K, gentle bounce light, no pure-black shadows, no neon colors. 16:9, 1080p, 25fps, '
    'no on-screen text, no subtitles, no watermark, no logos.')
STYLE_POLLUTION = ('Pollution grade for this shot: desaturate environment about 40%, hazy filtered light, palette smog grey #8A8D91, '
    'soot #3F4046, dust brown #A08C72, hazy sky #C9B9A0; keep characters readable and cute, never gross or scary.')
STYLE_GRAPHIC = ('Graphic style for this shot: "animation inside the animation", 2.5D paper-cut infographic layers, thick rounded outlines #2B2B3A, '
    'cream paper background #FFF8EC, bouncy squash-and-stretch motion, cute and simple shapes, blank label tags (text added in post).')

# ---------------------------------------------------------------- BỐI CẢNH
LOCS = {
    'BC01': dict(name='Sân trường tiểu học', scenes='1, 2, 3, 6, 7, 8, 9',
        desc='Sân trường tiểu học Việt Nam: bãi cỏ xanh rộng, cây bàng lớn tỏa bóng, bồn hoa viền gạch đỏ, cột cờ, dãy lớp học 2 tầng tường vàng mái ngói đỏ, hành lang lan can xanh lá, cổng trường sắt sơn xanh ở xa.',
        light='Nắng buổi sáng 9h, nắng ấm chếch 45°, bóng cây loang lổ trên cỏ. Cảnh 8–9: không khí trong vắt, có hạt sáng lấp lánh.',
        colors=['#8FD3FF', '#7CC66B', '#F2D27A', '#C8553D', '#FFE3A3'],
        prompt='Empty sunny Vietnamese primary school yard, wide green lawn, large Indian almond tree casting dappled shade, red-brick flower bed with small plants, flag pole, two-storey yellow classroom building with red tiled roof and green-railing corridors, green iron school gate in the far background, clear blue sky with soft white clouds, morning sunlight 45 degrees, no people. ' + STYLE_LOCK),
    'BC02': dict(name='Ngã tư kẹt xe', scenes='2',
        desc='Ngã tư phố Việt Nam giờ cao điểm: hàng dài xe máy, ô tô, xe buýt chen chúc; ống xả nhả khói; biển hiệu cửa hàng, cột điện chằng chịt dây.',
        light='Nắng bị lọc qua lớp mù khói, ám vàng xám, độ tương phản thấp.',
        colors=['#C9B9A0', '#8A8D91', '#3F4046', '#D9A441', '#6E6258'],
        prompt='Busy Vietnamese city intersection at rush hour seen from above, gridlocked motorbikes, cars and a bus, grey exhaust smoke rising, shophouses with signboards, tangled electric wires on poles, hazy filtered sunlight, no readable text. ' + STYLE_LOCK + ' ' + STYLE_POLLUTION),
    'BC03': dict(name='Công trình xây dựng', scenes='2, 4',
        desc='Công trình đang thi công bên đường: máy xúc vàng, cần cẩu tháp, đống cát, giàn giáo phủ lưới xanh, bụi đất cuộn bay ra phố.',
        light='Nắng gắt nhưng bị bụi làm mờ, tông nâu đất.',
        colors=['#A08C72', '#E8B33A', '#5E8C5A', '#8A8D91', '#C9B9A0'],
        prompt='Roadside construction site, yellow excavator digging, tower crane, sand piles, scaffolding wrapped in green safety net, thick brown dust clouds drifting onto the street, hazy light, no people in focus, no readable text. ' + STYLE_LOCK + ' ' + STYLE_POLLUTION),
    'BC04': dict(name='Đống rác bị đốt ven đường', scenes='2, 4',
        desc='Bãi đất trống ven đường, đống lá khô và túi ni lông đang cháy âm ỉ, cột khói đen bốc lên cao.',
        light='Ánh lửa cam nhỏ, khói đen che nắng, không khí đặc.',
        colors=['#3F4046', '#E07A2E', '#8A8D91', '#6E6258', '#C9B9A0'],
        prompt='Small vacant lot beside a road, pile of dry leaves and plastic bags burning slowly with small orange flames, thick dark smoke column rising, hazy grey sky, cartoon-clean not gross. ' + STYLE_LOCK + ' ' + STYLE_POLLUTION),
    'BC05': dict(name='Thế giới đồ họa (Animation in Animation)', scenes='4, 6',
        desc='Không gian đồ họa giấy cắt 2.5D trên nền kem: thành phố đồ chơi, xe cộ có mặt, cây cối có mắt. Dùng cho phần giải thích kiến thức.',
        light='Phẳng, đều, bóng đổ nhẹ giữa các lớp giấy.',
        colors=['#FFF8EC', '#2B2B3A', '#4CB050', '#3AA0E8', '#E8473C'],
        prompt='Cute 2.5D paper-cut infographic world on cream paper background, toy-like city blocks, rounded cars and buses with simple faces, tiny trees with blinking eyes, thick rounded outlines, layered paper shadows, empty space for labels, no text. ' + STYLE_GRAPHIC),
    'BC06': dict(name='Thế giới vi mô bụi mịn', scenes='5',
        desc='Không gian phóng đại: các hạt bụi PM2.5 bay lơ lửng như bong bóng tím; mặt cắt mũi và phổi kiểu hoạt hình hồng hào, dễ thương.',
        light='Tối nhẹ, ánh sáng xuyên thấu, hạt bụi có viền sáng.',
        colors=['#5B4B73', '#8A8D91', '#F7B5B0', '#FFFFFF', '#2B2B3A'],
        prompt='Microscopic cartoon world, floating dark purple dust particles like soft bubbles, gentle depth of field, light rays, cute stylized cross-section of a child\'s nose and pink lungs, educational but friendly, no gore, no text. ' + STYLE_LOCK),
    'BC07': dict(name='Sân sau nhà Bắp', scenes='7',
        desc='Sân sau nhà ống Việt Nam: tường vôi kem, chậu cây cảnh, 3 thùng rác phân loại (xanh lá – hữu cơ, xanh dương – tái chế, xám – còn lại), vòi nước, đống lá khô ở góc.',
        light='Nắng chiều ấm, bóng mềm.',
        colors=['#F3E6CF', '#4CB050', '#3AA0E8', '#8A8D91', '#FFE3A3'],
        prompt='Backyard of a Vietnamese tube house, cream plaster walls, potted plants, three colour-coded sorting bins (green, blue, grey), garden tap with a watering can, small pile of dry leaves in a corner, warm afternoon sunlight, no people. ' + STYLE_LOCK),
    'BC08': dict(name='Đường đến trường', scenes='7',
        desc='Con đường rợp bóng cây, làn xe đạp riêng, vỉa hè rộng, xe buýt xanh chạy êm phía xa.',
        light='Nắng sớm trong trẻo, tia nắng xuyên tán lá.',
        colors=['#8FD3FF', '#7CC66B', '#3AA0E8', '#FFE3A3', '#E3ECF6'],
        prompt='Tree-lined Vietnamese street in early morning, dedicated bicycle lane, wide clean sidewalk, sunbeams through green leaves, a clean blue city bus gliding in the background, fresh clear air. ' + STYLE_LOCK),
    'BC09': dict(name='Bầu trời mây trắng', scenes='1, 9',
        desc='Bầu trời xanh thẳm, đàn mây trắng lớn bồng bềnh — "nhà" của Mây Mây.',
        light='Ánh nắng trên cao, mây có viền sáng vàng nhạt.',
        colors=['#6EC3FA', '#8FD3FF', '#FFFFFF', '#E3ECF6', '#FFE3A3'],
        prompt='Deep clear blue sky with a family of large fluffy white cumulus clouds drifting, soft golden rim light, high altitude, peaceful, no birds, no text. ' + STYLE_LOCK),
    'BC10': dict(name='Trái Đất xanh (kết phim)', scenes='10',
        desc='Quả địa cầu xanh mướt xoay chậm giữa bầu trời rực rỡ, mây trắng bao quanh. Chừa khoảng trống giữa khung cho chữ thông điệp.',
        light='Sáng rực, chiếu từ sau tạo viền sáng.',
        colors=['#8FD3FF', '#4CB050', '#3AA0E8', '#FFFFFF', '#FFE3A3'],
        prompt='Cute stylized lush green planet Earth slowly rotating in a bright blue sky, white clouds orbiting around it, sparkles, glowing rim light, empty clean space in the centre third of the frame for a title, no text. ' + STYLE_LOCK),
}

# ---------------------------------------------------------------- KỊCH BẢN (nội dung gốc)
SCENES = [
    dict(n=1, tc='0:00 – 0:20', title='Sân trường – Trời nắng đẹp', loc=['BC01', 'BC09'],
        img=['Bé Bắp tung một chiếc máy bay giấy lên cao. Từ trên bầu trời xanh, một đám mây con (Mây Mây) trắng phau sà xuống, dùng chiếc bụng bông mềm mại đỡ lấy máy bay và "tâng" ngược lại cho Bắp.',
             'Mây Mây tinh nghịch cuộn tròn lại thành một quả bóng lơ lửng, bay là là quanh bãi cỏ. Bắp và nhóm bạn thích thú chạy đuổi theo, đưa tay chạm nhẹ vào người Mây Mây mềm nhún như kẹo bông gòn.',
             'Đang chơi đùa vui vẻ, bỗng một cơn gió to bất ngờ thổi thốc tới, cuốn Mây Mây bay tuột về hướng cổng trường.'],
        snd=[('Âm nhạc', 'Vui tươi, nhịp điệu rộn ràng.'), ('SFX', 'Tiếng "Boing!" ngộ nghĩnh khi đám mây tâng máy bay giấy. Tiếng bước chân lạo xạo trên cỏ và tiếng cười giòn tan của các bạn nhỏ.'),
             ('Bé Bắp', '(Reo lên thích thú) Ôi, một đám mây tí hon! Lại đây chơi cùng tụi mình nào!'), ('Mây Mây', '(Phát ra những tiếng "Tít tít, bíp bíp" vui vẻ.)'), ('SFX', 'Tiếng gió rít mạnh "Vù vù".')]),
    dict(n=2, tc='0:20 – 0:40', title='Biến cố ngoài cổng trường', loc=['BC02', 'BC03', 'BC04', 'BC01'],
        img=['Mây Mây lướt qua ngã tư kẹt xe ngập khói, một công trình đang tung bụi và một đống rác đang bị đốt.',
             'Bị khói bụi bủa vây, Mây Mây biến thành màu xám xịt, ho sặc sụa. Gió cuốn Mây Mây quay trở lại sân trường, rồi rơi "phịch" xuống bãi cỏ.',
             'Bé Bắp và nhóm bạn đang đứng đợi vội vàng chạy ào tới. Bắp quỳ sụp xuống, lo lắng dùng tay chạm nhẹ vào người Mây Mây. Đám mây rùng mình, yếu ớt thở ra một luồng khói xám nhạt khiến Bắp và các bạn phải lấy tay che mũi, nhăn mặt và bắt đầu ho khan.'],
        snd=[('SFX', 'Tiếng còi xe inh ỏi, động cơ gầm gừ. Tiếng máy xúc ồn ào.'), ('Mây Mây', '(Hoảng hốt, mắt mở to) Ơ... á! Khụ! Khụ!'), ('SFX', 'Tiếng rơi "phịch" nặng nề.'),
             ('Bé Bắp', '(Hốt hoảng) Ôi! Mây Mây! Cậu sao thế này?'), ('Nhóm bạn', '(Giật mình, lấy tay phẩy phẩy không khí) Khụ! Khụ! Mùi gì khét quá!')]),
    dict(n=3, tc='0:40 – 0:55', title='Khám bệnh cho Mây Mây', loc=['BC01'],
        img=['Bé Bắp nhanh trí lấy từ trong cặp ra một chiếc "kính lúp thám tử" to bự bằng nhựa. Cậu bé nheo một mắt, cẩn thận rọi kính lúp lướt dọc theo lớp vỏ xám ngoét, đang run rẩy của Mây Mây.',
             'Nhóm bạn thân cũng tò mò chụm đầu vào xem. Qua lăng kính lúp tròn, bề mặt bông xốp của Mây Mây không còn mịn màng nữa mà bám đầy những vệt lấm tấm đen sì, thỉnh thoảng lại bong ra vài hạt bụi li ti bay lơ lửng trong không khí.',
             'Các bạn nhỏ hít phải bụi, đồng loạt hắt xì hơi dây chuyền và lấy tay phẩy phẩy. Lúc này, cô giáo từ lớp bước ra, ân cần đặt tay lên vai Bắp mỉm cười.'],
        snd=[('Bé Bắp', '(Nheo mắt lẩm bẩm) Để thám tử Bắp ra tay!'), ('Bé Bắp', 'Trời ơi, trên người Mây Mây toàn những chấm đen kỳ lạ!'), ('Nhóm bạn', '(Đồng thanh) Hắt xì! Hắt xì!'),
             ('Cô giáo', 'Các thám tử nhí đang khám bệnh cho Mây Mây đấy à? Mây Mây bị ốm là do "ăn" phải quá nhiều khói bụi rồi!')]),
    dict(n=4, tc='0:55 – 1:20', title='Nguyên nhân ô nhiễm', loc=['BC05'],
        img=['Khung hình chuyển sang đồ họa sinh động (Animation in Animation). Màn hình chia làm các bối cảnh dễ thương nhưng đang bị "làm bẩn":',
             '– Những chiếc ô tô, xe máy nhả ra những "đám mây đen" có dán nhãn PM2.5, NO2.', '– Chiếc cần cẩu xây dựng rũ bụi xuống phố.', '– Một đống rác đang bốc khói khét lẹt.'],
        snd=[('Cô giáo (VO)', '(Diễn cảm) Các con biết không, một trong những nguyên nhân hàng đầu làm không khí bị ô nhiễm là do khói thải từ các phương tiện giao thông đấy. Bên cạnh đó, bụi từ các công trình xây dựng, hay hành động đốt rác ngoài đường cũng sinh ra vô số hạt bụi mịn siêu nhỏ...')]),
    dict(n=5, tc='1:20 – 1:40', title='Tác động đến sức khỏe', loc=['BC06'],
        img=['Đồ họa phóng to: Hạt bụi mịn PM2.5 được vẽ như một "tiểu yêu gai góc" nhưng ngốc nghếch. Nó bay lơ lửng, chui vào Mây Mây, khiến Mây Mây từ màu trắng phau bồng bềnh chuyển dần sang màu xám.'],
        snd=[('Cô giáo (VO)', 'Những hạt bụi mịn này rất láu cá! Chúng chui lọt qua mũi, đi thẳng vào phổi, làm Mây Mây ngạt thở và khiến chúng mình bị ho, ốm đấy!')]),
    dict(n=6, tc='1:40 – 2:00', title='Giải pháp sống xanh', loc=['BC01', 'BC05'],
        img=['Bé Bắp ngước lên nhìn cô giáo với ánh mắt quyết tâm.', 'Màn hình hiện lên các biểu tượng "Phép thuật sống xanh":',
             '– Một mầm cây nhỏ nhô lên khỏi mặt đất, vươn hai chiếc lá xanh mướt chớp chớp mắt.', '– Một chiếc xe buýt mặt cười vui vẻ và một đôi giày thể thao đang tung tăng bước đi.',
             '– Thùng rác màu xanh phân loại rác, kèm theo biển báo cấm đốt rác (hình ngọn lửa đỏ bị gạch chéo nhấp nháy).'],
        snd=[('Bé Bắp', 'Cô ơi, vậy giờ chúng con phải làm thế nào để Mây Mây khỏe trở lại ạ?'),
             ('Cô giáo', 'Chúng ta sẽ dùng "Phép thuật sống xanh"! Các con hãy cùng trồng thêm cây xanh. Thay vì đi xe máy, hãy rủ bố mẹ đi xe buýt hoặc đi bộ, đạp xe đến trường. Và tuyệt đối không đốt rác, xả rác bừa bãi nhé!')]),
    dict(n=7, tc='2:00 – 2:30', title='Chuỗi hành động thực tế', loc=['BC01', 'BC07', 'BC08'],
        img=['Dựng ngắn, nối tiếp nhau. Nhóm bạn tự giác đeo khẩu trang vừa khít mũi rồi tỏa đi hành động:', '– Một nhóm cùng cô giáo vun đất trồng các chậu cây nhỏ quanh bồn hoa.',
             '– Bé Bắp ở nhà vứt rác đúng nơi quy định và ngăn cản bố mẹ đang chuẩn bị đốt rác.', '– Một bạn nhỏ khác đạp xe đến trường.'],
        snd=[('Âm nhạc', 'Nhịp điệu dồn dập, tươi sáng, đầy cảm hứng.'), ('SFX', 'Tiếng xẻng xúc đất "lạo xạo". Tiếng nước xịt dập lửa. Tiếng chuông xe đạp, xe buýt chạy êm ru.')]),
    dict(n=8, tc='2:30 – 2:45', title='Sân trường – Mây Mây khỏe lại', loc=['BC01'],
        img=['Nguồn khói bụi biến mất. Không khí trong lành tràn ngập sân trường.', 'Mây Mây hít một hơi thật sâu. Lớp xám xịt bong ra. Mây Mây trở lại trắng phau, bồng bềnh và phát sáng lấp lánh.',
             'Bé Bắp mở to tròn đôi mắt ngạc nhiên, rồi vỡ òa sung sướng nhảy cẫng lên. Cả nhóm bạn nhảy múa, hò reo và đập tay (high-five) ăn mừng. Mây Mây vui sướng sà xuống, ôm chầm lấy Bắp, dụi dụi cái bụng bông xốp mềm mại vào má cậu bé trong vòng vây yêu thương của các bạn nhỏ.'],
        snd=[('SFX', 'Tiếng chuông gió leng keng (phép màu hồi sinh). Tiếng cười giòn tan của trẻ thơ.'), ('Mây Mây', '(Cười khúc khích)'), ('Nhóm bạn', '(Đồng thanh reo hò) Mây Mây trắng tinh lại rồi nè!')]),
    dict(n=9, tc='2:45 – 2:53', title='Lời chào tạm biệt', loc=['BC01', 'BC09'],
        img=['Mây Mây vẫy tay chào, nhẹ nhàng bay vút lên bầu trời xanh thẳm, nhập cùng đàn mây trắng. Các bạn nhỏ tháo khẩu trang, vẫy tay cười rạng rỡ.'],
        snd=[('SFX', 'Tiếng bay vút "Whoosh".'), ('Bắp & các bạn', 'Tạm biệt Mây Mây nhé!')]),
    dict(n=10, tc='2:53 – 3:00', title='Thông điệp kết thúc', loc=['BC10'],
        img=['Hình ảnh bầu trời rực rỡ và Trái Đất xanh mướt. Dòng chữ thông điệp lớn xuất hiện ở giữa màn hình.'],
        snd=[('Voice-over', '(Giọng trẻ em vang, dõng dạc) "Không khí sạch là lá chắn cho sức khỏe. Hãy cùng hành động để bầu trời luôn xanh!"'), ('Âm nhạc', 'Nhỏ dần rồi kết thúc (fade out).')]),
]

# ---------------------------------------------------------------- SHOT LIST / PROMPT SEEDANCE 2.0
def C(*k):
    return list(k)

SHOTS = [
    dict(id='1.1', sc=1, tc='0:00–0:10', use=10, chars=C('bap', 'na', 'su', 'may'), loc=['BC01', 'BC09'], mode='day',
        vi='Bắp tung máy bay giấy, Mây Mây sà xuống đỡ bằng bụng bông và tâng ngược lại cho Bắp.',
        audio='Nhạc vui rộn ràng · SFX "Boing!" · Bắp: "Ôi, một đám mây tí hon! Lại đây chơi cùng tụi mình nào!"',
        beats=['0–3s: Wide shot of a sunny Vietnamese primary school yard. Bap runs across the green lawn and throws a white paper airplane high into the blue sky; Na and Su cheer behind him.',
               '3–6s: Camera tilts up following the plane. From the sky, Mây Mây swoops down and catches the plane on its soft cotton belly, which squishes like a trampoline.',
               '6–10s: Mây Mây bounces the plane back ("boing"), it glides down into Bap\'s hands. Medium close-up: Bap looks up, amazed and delighted, and calls out to the cloud.'],
        cam='Wide establishing shot, smooth tilt up, then push-in to medium close-up on Bap.',
        sound='Cheerful marimba and ukulele music, cartoon "boing" sound, kids laughing. Bap shouts happily in Vietnamese: "Ôi, một đám mây tí hon! Lại đây chơi cùng tụi mình nào!"'),
    dict(id='1.2', sc=1, tc='0:10–0:20', use=10, chars=C('bap', 'na', 'su', 'may'), loc=['BC01'], mode='day',
        vi='Mây Mây cuộn tròn thành quả bóng bay là là, các bạn đuổi theo chạm vào. Cơn gió to cuốn Mây Mây về phía cổng trường.',
        audio='Mây Mây "tít tít, bíp bíp" · bước chân trên cỏ · tiếng gió "vù vù"',
        beats=['0–4s: Mây Mây curls into a round fluffy ball and floats low around the lawn, beeping playfully. Bap, Na and Su chase it, laughing.',
               '4–7s: The kids gently poke Mây Mây; its body squishes softly like cotton candy and springs back. Mây Mây giggles.',
               '7–10s: Suddenly a strong gust of wind bends the almond tree, leaves fly; Mây Mây is swept away fast toward the school gate. The kids stop and reach out, surprised.'],
        cam='Low tracking shot running with the kids at grass level, whip pan following Mây Mây toward the gate.',
        sound='Playful music, footsteps on grass, Mây Mây beeps "tít tít, bíp bíp", then a strong wind "whoosh" sound.'),
    dict(id='2.1', sc=2, tc='0:20–0:30', use=10, chars=C('may'), loc=['BC02', 'BC03', 'BC04'], mode='poll',
        vi='Mây Mây bị gió cuốn qua ngã tư kẹt xe, công trình tung bụi, đống rác đốt — dần chuyển xám, ho sặc sụa.',
        audio='Còi xe inh ỏi, động cơ gầm gừ, máy xúc · Mây Mây: "Ơ... á! Khụ! Khụ!"',
        beats=['0–3s: Mây Mây tumbles through the air over a gridlocked intersection; motorbikes and cars puff grey exhaust that wraps around it.',
               '3–6s: It drifts past a construction site; an excavator throws up brown dust clouds into its face.',
               '6–10s: It passes over a burning trash pile; thick dark smoke engulfs it. Mây Mây turns dirty grey with black soot specks, eyes wide in panic, coughing hard.'],
        cam='Continuous side-tracking shot flying alongside Mây Mây at rooftop height, ending on a close-up of its face.',
        sound='Loud honking, engines roaring, excavator noise. Mây Mây gasps in Vietnamese: "Ơ... á! Khụ! Khụ!"',
        extra=['grey']),
    dict(id='2.2', sc=2, tc='0:30–0:40', use=10, chars=C('may', 'bap', 'na', 'su'), loc=['BC01'], mode='poll_soft',
        vi='Mây Mây xám rơi "phịch" xuống bãi cỏ. Các bạn chạy tới, Bắp quỳ xuống chạm vào. Mây Mây thở ra khói xám, các bạn che mũi, ho.',
        audio='SFX "phịch" · Bắp: "Ôi! Mây Mây! Cậu sao thế này?" · Nhóm bạn: "Khụ! Khụ! Mùi gì khét quá!"',
        beats=['0–3s: The wind carries the grey Mây Mây back over the school wall; it drops heavily onto the lawn with a thud and a small puff of dust.',
               '3–6s: Bap, Na and Su run in. Bap kneels down and gently touches the trembling grey cloud, worried.',
               '6–10s: Mây Mây shivers and weakly exhales a puff of light grey smoke. The kids cover their noses, grimace, cough and wave the air away.'],
        cam='High angle as it falls, then low angle close on Bap kneeling, cut to a two-shot of Na and Su coughing.',
        sound='Heavy "thud". Bap in Vietnamese, alarmed: "Ôi! Mây Mây! Cậu sao thế này?" Na and Su coughing: "Khụ! Khụ! Mùi gì khét quá!"',
        extra=['grey']),
    dict(id='3.1', sc=3, tc='0:40–0:47', use=7, chars=C('bap', 'na', 'su', 'may'), loc=['BC01'], mode='day',
        vi='Bắp lấy kính lúp thám tử, nheo mắt soi Mây Mây. Qua lăng kính: bề mặt bám đầy chấm đen, bụi li ti bong ra.',
        audio='Bắp: "Để thám tử Bắp ra tay!" ... "Trời ơi, trên người Mây Mây toàn những chấm đen kỳ lạ!"',
        beats=['0–3s: Bap pulls a big red plastic toy detective magnifying glass out of his backpack, squints one eye with a determined grin.',
               '3–6s: He slowly sweeps the glass along the trembling grey body of Mây Mây; Na and Su lean in, heads together, curious.',
               '6–10s: POV through the round lens: macro view of the fluffy surface covered in black soot specks; tiny dust particles flake off and float in the air.'],
        cam='Close-up on Bap, slow lateral move, then lens-shaped POV macro insert.',
        sound='Light curious pizzicato music. Bap mutters in Vietnamese: "Để thám tử Bắp ra tay!" then gasps: "Trời ơi, trên người Mây Mây toàn những chấm đen kỳ lạ!"',
        extra=['grey']),
    dict(id='3.2', sc=3, tc='0:47–0:55', use=8, chars=C('na', 'su', 'bap', 'co', 'may'), loc=['BC01'], mode='day',
        vi='Các bạn hắt xì dây chuyền. Cô giáo bước ra từ lớp, đặt tay lên vai Bắp, mỉm cười giải thích.',
        audio='Nhóm bạn: "Hắt xì! Hắt xì!" · Cô giáo: "Các thám tử nhí đang khám bệnh cho Mây Mây đấy à? Mây Mây bị ốm là do \'ăn\' phải quá nhiều khói bụi rồi!"',
        beats=['0–3s: The floating dust reaches the kids; Na sneezes, then Su, in a funny chain reaction, waving their hands.',
               '3–5s: The Teacher walks out from the classroom corridor, kneels beside Bap and gently places a hand on his shoulder, smiling.',
               '5–10s: Medium shot of the Teacher talking warmly to the kids, the grey Mây Mây resting on the grass in front of them.'],
        cam='Quick comedic cuts on sneezes, then a calm medium shot at child eye level.',
        sound='Sneezes "Hắt xì! Hắt xì!". The Teacher speaks gently in Vietnamese: "Các thám tử nhí đang khám bệnh cho Mây Mây đấy à? Mây Mây bị ốm là do ăn phải quá nhiều khói bụi rồi!"',
        extra=['grey']),
    dict(id='4.1', sc=4, tc='0:55–1:03', use=8, chars=[], loc=['BC05'], mode='graphic',
        vi='Đồ họa: ô tô, xe máy đồ chơi có mặt nhả ra "đám mây đen" dán nhãn PM2.5, NO2.',
        audio='Cô giáo (VO): "Các con biết không, một trong những nguyên nhân hàng đầu làm không khí bị ô nhiễm là do khói thải từ các phương tiện giao thông đấy."',
        beats=['0–4s: A cute paper-cut street slides in; rounded cars and motorbikes with simple faces drive along, coughing out grumpy dark smoke clouds.',
               '4–10s: The smoke clouds gather into a big sulky black cloud with two blank label tags hanging from it (labels PM2.5 and NO2 to be added in post), it frowns over the street.'],
        cam='Flat side view, slow parallax pan left to right.',
        sound='Light educational music, cartoon putt-putt engine sounds. Female narrator voice-over in Vietnamese, warm and expressive (dub in post).'),
    dict(id='4.2', sc=4, tc='1:03–1:11', use=8, chars=[], loc=['BC05', 'BC03'], mode='graphic',
        vi='Đồ họa: cần cẩu xây dựng rũ bụi xuống phố.',
        audio='Cô giáo (VO): "Bên cạnh đó, bụi từ các công trình xây dựng..."',
        beats=['0–4s: A paper-cut construction site pops up; a friendly tower crane shakes a big sack like a rug.',
               '4–10s: Brown dust pours down onto the little street like flour; tiny houses and trees squint and cover their faces.'],
        cam='Flat front view, gentle zoom out.',
        sound='Clanking crane sounds, soft "poof" dust sounds, narrator voice-over continues (dub in post).'),
    dict(id='4.3', sc=4, tc='1:11–1:20', use=9, chars=[], loc=['BC05', 'BC04'], mode='graphic',
        vi='Đồ họa: đống rác bốc khói khét lẹt, sinh ra vô số hạt bụi mịn siêu nhỏ.',
        audio='Cô giáo (VO): "...hay hành động đốt rác ngoài đường cũng sinh ra vô số hạt bụi mịn siêu nhỏ..."',
        beats=['0–4s: A paper-cut trash pile with a small cartoon flame on top puffs out a thick wobbly smoke column.',
               '4–9s: The smoke breaks apart into hundreds of tiny purple dots that multiply and spread across the screen, filling the sky.'],
        cam='Flat front view, slow push-in on the smoke turning into particles.',
        sound='Crackling fire, sizzling, rising mysterious synth, narrator voice-over continues (dub in post).'),
    dict(id='5.1', sc=5, tc='1:20–1:30', use=10, chars=C('may'), loc=['BC06'], mode='micro',
        vi='Phóng to: tiểu yêu PM2.5 gai góc nhưng ngốc nghếch bay lơ lửng, chui vào Mây Mây khiến Mây Mây chuyển dần từ trắng sang xám.',
        audio='Cô giáo (VO): "Những hạt bụi mịn này rất láu cá!" · SFX cười khúc khích lém lỉnh',
        beats=['0–3s: Extreme close-up: a single PM2.5 gremlin floats into frame, rolls its mismatched eyes and grins goofily.',
               '3–7s: Dozens of gremlins float in a wobbly line and dive one by one into the white fluffy body of Mây Mây, like jumping into a pillow.',
               '7–10s: Mây Mây slowly turns from bright white to grey, starting from the edges inward, its smile fading into a worried look.'],
        cam='Macro lens feel, shallow depth of field, slow orbit around Mây Mây.',
        sound='Mischievous pizzicato, tiny gremlin giggles "hi hi hi". Narrator voice-over in Vietnamese (dub in post).',
        extra=['gremlin']),
    dict(id='5.2', sc=5, tc='1:30–1:40', use=10, chars=C('bap'), loc=['BC06'], mode='micro',
        vi='Đồ họa mặt cắt: tiểu yêu PM2.5 chui lọt qua mũi, đi thẳng vào phổi; Bắp ho.',
        audio='Cô giáo (VO): "Chúng chui lọt qua mũi, đi thẳng vào phổi, làm Mây Mây ngạt thở và khiến chúng mình bị ho, ốm đấy!"',
        beats=['0–3s: Side profile of Bap breathing in; a few PM2.5 gremlins sneak past his nose.',
               '3–7s: Cute transparent cross-section: the gremlins slide down the airway like a water slide into pink cartoon lungs, which frown and puff.',
               '7–10s: Back to Bap: he coughs twice and rubs his nose, uncomfortable.'],
        cam='Profile medium close-up, dissolve into cross-section diagram, back to close-up.',
        sound='Whoosh slide sounds, small cough sounds. Narrator voice-over in Vietnamese (dub in post).',
        extra=['gremlin']),
    dict(id='6.1', sc=6, tc='1:40–1:48', use=8, chars=C('bap', 'co', 'na', 'su', 'may'), loc=['BC01'], mode='day',
        vi='Bắp ngước lên nhìn cô giáo với ánh mắt quyết tâm và hỏi. Cô mỉm cười, giơ ngón tay — tia lấp lánh xanh lá.',
        audio='Bắp: "Cô ơi, vậy giờ chúng con phải làm thế nào để Mây Mây khỏe trở lại ạ?" · Cô: "Chúng ta sẽ dùng \'Phép thuật sống xanh\'!"',
        beats=['0–4s: Bap holds the grey Mây Mây gently in his arms and looks up at the Teacher with determined eyes, asking a question; Na and Su nod beside him.',
               '4–8s: The Teacher smiles, raises one finger; tiny green leaf-shaped sparkles swirl around her fingertip as she answers.'],
        cam='Low angle from Bap\'s point of view up to the Teacher, then reverse shot.',
        sound='Hopeful music swell. Bap in Vietnamese: "Cô ơi, vậy giờ chúng con phải làm thế nào để Mây Mây khỏe trở lại ạ?" Teacher: "Chúng ta sẽ dùng Phép thuật sống xanh!" Magic sparkle sound.',
        extra=['grey']),
    dict(id='6.2', sc=6, tc='1:48–2:00', use=10, chars=[], loc=['BC05'], mode='graphic',
        vi='Đồ họa "Phép thuật sống xanh": mầm cây chớp mắt, xe buýt mặt cười và giày thể thao, thùng rác phân loại + biển cấm đốt rác nhấp nháy. (Giữ khung cuối 2s.)',
        audio='Cô giáo (VO): "Các con hãy cùng trồng thêm cây xanh. Thay vì đi xe máy, hãy rủ bố mẹ đi xe buýt hoặc đi bộ, đạp xe đến trường. Và tuyệt đối không đốt rác, xả rác bừa bãi nhé!"',
        beats=['0–3s: A tiny sprout pops out of the soil, unfolds two bright green leaves and blinks its eyes happily.',
               '3–6s: A smiling blue bus drives by, followed by a pair of sneakers hopping along cheerfully.',
               '6–10s: A green sorting trash bin waves; beside it a round red "no burning" sign (flame crossed out) blinks on and off.'],
        cam='Flat graphic layout, each icon pops in with squash-and-stretch, light camera slide between them.',
        sound='Bright magical music, "pop" sound for each icon, bus horn "beep beep", narrator voice-over (dub in post).'),
    dict(id='7.1', sc=7, tc='2:00–2:10', use=10, chars=C('na', 'su', 'bap', 'co'), loc=['BC01'], mode='day',
        vi='Các bạn đeo khẩu trang vừa khít mũi. Na, Su cùng cô giáo vun đất, trồng chậu cây nhỏ quanh bồn hoa.',
        audio='Nhạc dồn dập, tươi sáng · SFX xẻng xúc đất "lạo xạo"',
        beats=['0–3s: Close-up: Bap, Na and Su put on light blue face masks and press the nose clip to fit snugly, then give each other a thumbs-up.',
               '3–10s: At the red-brick flower bed, the Teacher and Na dig soil with small shovels and plant little potted seedlings; Su waters them with a green watering can. Everyone smiles behind their masks.'],
        cam='Quick montage cuts, then a medium wide shot of the flower bed, slight handheld energy.',
        sound='Upbeat energetic music, shovel scraping soil, water sprinkling.'),
    dict(id='7.2', sc=7, tc='2:10–2:20', use=10, chars=C('bap'), loc=['BC07'], mode='day',
        vi='Ở nhà, Bắp bỏ rác đúng thùng phân loại, rồi chạy tới ngăn bố mẹ đang chuẩn bị đốt đống lá và ni lông, dội nước dập lửa.',
        audio='SFX nước xịt dập lửa "xèo" · nhạc dồn dập',
        beats=['0–3s: In the backyard Bap, wearing his mask, drops a plastic bottle into the blue recycling bin and banana peels into the green bin.',
               '3–6s: He turns and sees his Dad about to light a pile of dry leaves and plastic bags with a lighter, Mom holding a trash bag next to him.',
               '6–10s: Bap runs over, waves his arms "stop!", and pours a watering can on the tiny flame (fizz). Dad and Mom laugh sheepishly, nod and put the trash into the bins.'],
        cam='Medium shot, quick pan to the parents, comedic push-in on Bap\'s "stop" pose.',
        sound='Upbeat music, bottle clunk, water fizz on fire, parents laughing.',
        extra=['parents']),
    dict(id='7.3', sc=7, tc='2:20–2:30', use=10, chars=C('su'), loc=['BC08'], mode='day',
        vi='Su đội mũ bảo hiểm xe đạp, đeo khẩu trang, đạp xe đến trường trên làn xe đạp; xe buýt xanh chạy êm bên cạnh.',
        audio='SFX chuông xe đạp "kính coong", xe buýt chạy êm ru',
        beats=['0–4s: Su rides a small bicycle along a tree-lined bike lane, wearing a white kid\'s helmet and a light blue face mask, sunbeams through the leaves.',
               '4–7s: He rings the bell happily; a clean blue city bus full of smiling passengers glides past quietly.',
               '7–10s: Su arrives at the green school gate and waves at the camera.'],
        cam='Side tracking shot alongside the bicycle, then front shot at the gate.',
        sound='Cheerful music, bicycle bell "ring ring", soft electric bus hum, birds chirping.'),
    dict(id='8.1', sc=8, tc='2:30–2:38', use=8, chars=C('may', 'bap', 'na', 'su'), loc=['BC01'], mode='glow',
        vi='Không khí trong lành. Mây Mây hít sâu, lớp xám bong ra, trở lại trắng phau, phát sáng lấp lánh. Bắp tròn mắt ngạc nhiên.',
        audio='SFX chuông gió leng keng (phép màu hồi sinh)',
        beats=['0–3s: The school yard air turns crystal clear with tiny floating light sparkles. Grey Mây Mây floats up from the grass and takes a big deep breath.',
               '3–6s: The grey shell cracks and peels away like ash petals that dissolve into light; underneath, Mây Mây is bright pure white and softly glowing.',
               '6–8s: Bap, Na and Su (masks on) stare with wide round eyes, amazed.'],
        cam='Slow push-in on Mây Mây, soft lens bloom, cut to the kids\' reaction shot.',
        sound='Magical wind chimes, rising strings.',
        extra=['grey', 'glow']),
    dict(id='8.2', sc=8, tc='2:38–2:45', use=7, chars=C('bap', 'na', 'su', 'may'), loc=['BC01'], mode='glow',
        vi='Bắp nhảy cẫng lên, cả nhóm nhảy múa, đập tay ăn mừng. Mây Mây sà xuống ôm chầm Bắp, dụi bụng bông vào má cậu.',
        audio='Mây Mây cười khúc khích · Nhóm bạn: "Mây Mây trắng tinh lại rồi nè!"',
        beats=['0–3s: Bap jumps for joy; Na and Su dance and high-five each other.',
               '3–7s: Glowing white Mây Mây swoops down and hugs Bap, nuzzling its fluffy belly against his cheek; Na and Su circle around them, cheering.'],
        cam='Medium shot, gentle circling camera around the group.',
        sound='Joyful music, children laughing, Mây Mây giggling. Kids shout in Vietnamese: "Mây Mây trắng tinh lại rồi nè!"',
        extra=['glow']),
    dict(id='9.1', sc=9, tc='2:45–2:53', use=8, chars=C('may', 'bap', 'na', 'su', 'co'), loc=['BC01', 'BC09'], mode='day',
        vi='Mây Mây vẫy tay, bay vút lên bầu trời, nhập đàn mây trắng. Các bạn tháo khẩu trang, vẫy tay cười rạng rỡ.',
        audio='SFX "Whoosh" · Bắp & các bạn: "Tạm biệt Mây Mây nhé!"',
        beats=['0–3s: Mây Mây waves its little hands, then zooms up into the deep blue sky.',
               '3–6s: The kids take off their masks and wave, beaming; the Teacher stands behind them smiling.',
               '6–8s: High in the sky, Mây Mây joins a family of big white clouds, which hug it gently.'],
        cam='Crane up from the kids to the sky, following Mây Mây.',
        sound='Whoosh. Kids together in Vietnamese: "Tạm biệt Mây Mây nhé!" Music softens.'),
    dict(id='10.1', sc=10, tc='2:53–3:00', use=7, chars=[], loc=['BC10'], mode='day',
        vi='Bầu trời rực rỡ, Trái Đất xanh mướt xoay chậm. Chừa khoảng giữa khung để chèn chữ thông điệp ở hậu kỳ.',
        audio='Voice-over trẻ em: "Không khí sạch là lá chắn cho sức khỏe. Hãy cùng hành động để bầu trời luôn xanh!" · nhạc fade out',
        beats=['0–7s: A lush green cartoon Earth slowly rotates in a bright blue sky, white clouds orbiting and sparkling. Keep the centre of the frame clean and calm for a title card.'],
        cam='Slow dolly-in, very stable, ends on a still frame.',
        sound='Uplifting final chord, fading out. Child voice-over (dub in post).'),
]

MODE_STYLE = {'day': '', 'poll': STYLE_POLLUTION, 'poll_soft': 'Light lingering haze around Mây Mây only, the school yard stays sunny.',
              'graphic': STYLE_GRAPHIC, 'micro': 'Microscopic close-up world with soft light rays and shallow depth of field.',
              'glow': 'Air is crystal clear, golden rim light #FFE3A3, tiny sparkles, slight bloom.'}
EXTRA_LOCK = {'grey': EXTRA_CHARS[0][2], 'glow': EXTRA_CHARS[1][2], 'gremlin': EXTRA_CHARS[2][2], 'parents': EXTRA_CHARS[3][2]}

def build_prompt(s):
    lines = []
    if s['chars']:
        lines.append('References: ' + '; '.join(CHARS[k]['lock'] for k in s['chars']) + '.')
    for x in s.get('extra', []):
        lines.append(EXTRA_LOCK[x])
    lines.append('Location: ' + LOCS[s['loc'][0]]['name_en'] + '.')
    lines.append(f"Duration: 10 seconds, 16:9. (Edit uses {s['use']}s.)")
    lines += s['beats']
    lines.append('Camera: ' + s['cam'])
    lines.append('Audio: ' + s['sound'])
    if MODE_STYLE[s['mode']]:
        lines.append(MODE_STYLE[s['mode']])
    lines.append(STYLE_LOCK)
    return '\n'.join(lines)

NAME_EN = {'BC01': 'sunny Vietnamese primary school yard with green lawn, big Indian almond tree, red-brick flower bed, yellow two-storey classroom building with red tiled roof',
           'BC02': 'gridlocked Vietnamese city intersection, then a roadside construction site, then a burning trash pile on a vacant lot (see beats)',
           'BC03': 'roadside construction site with crane and dust', 'BC04': 'burning trash pile beside a road',
           'BC05': '2.5D paper-cut infographic world on cream paper background',
           'BC06': 'microscopic cartoon world of floating fine dust particles',
           'BC07': 'backyard of a Vietnamese tube house with three colour-coded sorting bins and a pile of dry leaves',
           'BC08': 'tree-lined Vietnamese street with a dedicated bicycle lane in the early morning',
           'BC09': 'deep blue sky with big white clouds', 'BC10': 'bright blue sky with a lush green cartoon Earth'}
for k, v in LOCS.items():
    v['name_en'] = NAME_EN[k]

# ---------------------------------------------------------------- HTML
def chip(k):
    c = CHARS[k]
    return f'<span class="chip"><i class="av av-{k}"></i>{E(c["name"])}<b>{c["ref"]}</b></span>'

def locchip(k):
    return f'<a class="chip loc" href="#boi-canh" data-goto="{k}"><span class="loc-id">{k}</span>{E(LOCS[k]["name"])}</a>'

css_imgs = '\n'.join(f'.av-{k}{{background-image:url({b64(CHARS[k]["file"])})}}' for k in ORDER)

# Tab 1: Tổng quan
total_used = sum(s['use'] for s in SHOTS)
char_cards = ''.join(f'''
<article class="char">
  <div class="sheet av-{k}" role="img" aria-label="Sheet nhân vật {E(CHARS[k]['name'])}"></div>
  <div class="char-body">
    <header><h3>{E(CHARS[k]['name'])}</h3><span class="ref">{CHARS[k]['ref']}</span></header>
    <p class="role">{E(CHARS[k]['role'])}</p>
    <dl>
      <dt>Tính cách</dt><dd>{E(CHARS[k]['trait'])}</dd>
      <dt>Ngoại hình khóa</dt><dd>{E(CHARS[k]['look'])}</dd>
      <dt>Giọng</dt><dd>{E(CHARS[k]['voice'])}</dd>
    </dl>
  </div>
</article>''' for k in ORDER)

extra_cards = ''.join(f'<li><strong>{E(n)}</strong><span>{E(d)}</span></li>' for n, d, _ in EXTRA_CHARS)

def sw(hexv, name, use):
    return f'<li class="sw"><span class="dot" style="background:{hexv}"></span><span class="sw-t"><b>{E(name)}</b><code>{hexv}</code><small>{E(use)}</small></span></li>'

palette_html = ''.join(f'<section class="pal"><h4>{E(t)}</h4><ul class="sws">{"".join(sw(*c) for c in cols)}</ul></section>' for t, cols in PALETTE)
cscript = ''.join(f'<li><span class="cs-bar" style="background:linear-gradient(180deg,{a} 0 62%,{b} 62% 100%)"></span><b>C{n}</b><span>{E(t)}</span><small>{E(m)}</small></li>' for n, t, a, b, m in COLOR_SCRIPT)

timeline = ''.join(f'<a class="tl-seg" href="#noi-dung" data-goto="scene-{s["n"]}" style="flex:{sum(x["use"] for x in SHOTS if x["sc"]==s["n"])}" title="Cảnh {s["n"]}: {E(s["title"])} ({s["tc"]})"><b>{s["n"]}</b></a>' for s in SCENES)

tab_overview = f'''
<section class="hero panel">
  <div class="hero-copy">
    <p class="eyebrow">Kịch bản sản xuất · Hoạt hình 3D · Series giáo dục môi trường</p>
    <h1>Mây Mây Đi Lạc</h1>
    <p class="logline">Một đám mây con trắng phau rơi xuống sân trường tiểu học, bị khói bụi thành phố làm cho ngạt thở và xám xịt. Cậu bé Bắp cùng các bạn và cô giáo dùng "Phép thuật sống xanh" để chữa lành cho Mây Mây.</p>
    <p class="msg"><span>Thông điệp</span>"Không khí sạch là lá chắn cho sức khỏe. Hãy cùng hành động để bầu trời luôn xanh!"</p>
  </div>
  <div class="hero-cast" aria-hidden="true">
    <i class="av av-may big"></i><i class="av av-bap"></i><i class="av av-na"></i><i class="av av-su"></i><i class="av av-co"></i>
  </div>
</section>

<section class="specs">
  <div><span>Thời lượng</span><b>3:00</b><small>10 cảnh · {len(SHOTS)} shot</small></div>
  <div><span>Độ phân giải</span><b>1920×1080</b><small>16:9 Full HD</small></div>
  <div><span>Khung hình</span><b>25 fps</b><small>Theo yêu cầu 25/30</small></div>
  <div><span>Định dạng</span><b>MP4 H.264</b><small>Bản có & không phụ đề</small></div>
  <div><span>Công cụ video</span><b>Seedance 2.0</b><small>Mỗi shot 10 giây</small></div>
  <div><span>Khán giả</span><b>Tiểu học</b><small>6–10 tuổi</small></div>
</section>

<section class="panel">
  <h2>Nhịp phim</h2>
  <p class="note">Độ dài mỗi đoạn tính theo thời lượng dựng thực tế. Bấm vào một cảnh để xem nội dung.</p>
  <div class="timeline">{timeline}</div>
  <div class="tl-scale"><span>0:00</span><span>1:00</span><span>2:00</span><span>3:00</span></div>
</section>

<section class="panel">
  <h2>Nhân vật</h2>
  <p class="note">Mỗi nhân vật có một mã tham chiếu cố định. Khi tạo video trên Seedance 2.0, luôn tải 5 ảnh sheet theo đúng thứ tự @Image1 → @Image5 để mã trong prompt khớp với ảnh.</p>
  <div class="chars">{char_cards}</div>
  <h3 class="sub">Biến thể và nhân vật phụ</h3>
  <ul class="extras">{extra_cards}</ul>
</section>

<section class="panel locked">
  <div class="lock-head">
    <h2>Bảng màu phim</h2>
    <span class="lock-badge"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 7V5a4 4 0 0 1 8 0v2h1v8H3V7h1zm2 0h4V5a2 2 0 0 0-4 0v2z"/></svg>Đã khóa</span>
  </div>
  <p class="note">Bảng màu này cố định cho toàn bộ phim. Mọi prompt đều chèn đoạn Style lock bên dưới. Không thêm màu ngoài bảng, không dùng màu neon, không đổ bóng đen tuyền.</p>
  <div class="pals">{palette_html}</div>
  <h3 class="sub">Kịch bản màu theo cảnh</h3>
  <ol class="cscript">{cscript}</ol>
  <h3 class="sub">Ánh sáng</h3>
  <ul class="rules">
    <li><b>Ngày đẹp trời</b> Nắng 5600K chếch 45°, ánh sáng phản xạ mềm, độ bão hòa +10%.</li>
    <li><b>Ô nhiễm</b> Ánh sáng lọc qua mù khói, giảm bão hòa môi trường 40%, giữ nhân vật dễ thương, không ghê sợ.</li>
    <li><b>Hồi phục</b> Không khí trong vắt, viền sáng vàng #FFE3A3, hạt lấp lánh, bloom nhẹ.</li>
    <li><b>Đồ họa</b> Phẳng 2.5D, nền giấy kem, viền dày bo tròn, chữ chèn ở hậu kỳ.</li>
  </ul>
  <div class="prompt-box">
    <div class="pb-head"><span>Style lock (chèn vào mọi prompt)</span><button type="button" class="copy" data-copy="style-lock">Sao chép</button></div>
    <pre id="style-lock">{E(STYLE_LOCK)}</pre>
  </div>
</section>

<section class="panel">
  <h2>Ghi chú sản xuất</h2>
  <ul class="rules">
    <li><b>Lồng tiếng</b> Seedance 2.0 có thể tạo khẩu hình và âm thanh, nhưng thoại tiếng Việt nên thu và lồng ở hậu kỳ để đúng dấu, đúng giọng. Prompt vẫn ghi câu thoại để nhân vật khớp khẩu hình.</li>
    <li><b>Chữ trên màn hình</b> Nhãn PM2.5, NO2, biển báo và thông điệp cuối phim làm bằng đồ họa ở hậu kỳ. AI không hiển thị chính xác chữ tiếng Việt có dấu.</li>
    <li><b>Thời lượng</b> Mỗi shot tạo 10 giây, cột "Dùng" ghi số giây cắt vào phim. Tổng thời lượng dựng: {total_used // 60}:{total_used % 60:02d}.</li>
    <li><b>Đồng nhất</b> Khóa seed khi một shot đạt. Dùng khung cuối của shot trước làm ảnh đầu cho shot sau trong cùng cảnh.</li>
    <li><b>Cần bổ sung</b> Sheet cho tiểu yêu PM2.5 và bố mẹ Bắp. Tên Na và Su là tên đề xuất, kịch bản gốc chỉ ghi "nhóm bạn".</li>
  </ul>
</section>
'''

# Tab 2: Nội dung
def scene_block(s):
    shots = [x for x in SHOTS if x['sc'] == s['n']]
    cs = []
    for x in shots:
        for k in x['chars']:
            if k not in cs:
                cs.append(k)
    imgs = ''.join(f'<p>{E(p)}</p>' for p in s['img'])
    snds = ''.join(f'<li><b>{E(w)}</b><span>{E(t)}</span></li>' for w, t in s['snd'])
    shot_ids = ' · '.join(f'<a href="#prompt" data-goto="shot-{x["id"]}">{x["id"]}</a>' for x in shots)
    return f'''
<article class="scene panel" id="scene-{s['n']}">
  <header class="scene-head">
    <span class="scene-n">{s['n']}</span>
    <div><h3>{E(s['title'])}</h3><p class="tc">{s['tc']} · Shot {shot_ids}</p></div>
  </header>
  <div class="scene-meta">
    <div><span class="lbl">Nhân vật</span><div class="chips">{''.join(chip(k) for k in cs) or '<span class="none">Đồ họa, không có nhân vật chính</span>'}</div></div>
    <div><span class="lbl">Bối cảnh</span><div class="chips">{''.join(locchip(k) for k in s['loc'])}</div></div>
  </div>
  <div class="scene-cols">
    <div class="col"><h4>Hình ảnh</h4>{imgs}</div>
    <div class="col"><h4>Âm thanh & thoại</h4><ul class="snd">{snds}</ul></div>
  </div>
</article>'''

tab_content = f'''
<section class="panel intro">
  <h2>Nội dung kịch bản</h2>
  <p>Series hoạt hình ngắn "Mây Mây Đi Lạc" kể về hành trình một đám mây con trắng phau từ trên trời rơi xuống sân trường tiểu học và bị khói bụi thành phố làm cho ngạt thở, xám xịt. Được sự giúp đỡ của cậu bé Bắp cùng các bạn học sinh, Mây Mây đã được chữa lành nhờ những chậu cây xanh và chiến dịch bảo vệ môi trường thiết thực. Qua đó, bộ phim truyền tải thông điệp nhân văn: hãy cùng nhau giữ gìn không khí sạch để bầu trời và thiên nhiên luôn được thở khỏe mạnh.</p>
  <ol class="acts">
    <li><b>Hồi 1 · Gặp gỡ</b><span>Cảnh 1 · 0:00–0:20</span></li>
    <li><b>Hồi 2 · Biến cố và kiến thức</b><span>Cảnh 2–6 · 0:20–2:00</span></li>
    <li><b>Hồi 3 · Hành động và hồi phục</b><span>Cảnh 7–10 · 2:00–3:00</span></li>
  </ol>
</section>
{''.join(scene_block(s) for s in SCENES)}
'''

# Tab 3: Prompt
def shot_card(x):
    p = build_prompt(x)
    chars = ''.join(chip(k) for k in x['chars']) or '<span class="none">Không có nhân vật chính</span>'
    for e in x.get('extra', []):
        label = {'grey': 'Mây Mây (xám)', 'glow': 'Mây Mây (phát sáng)', 'gremlin': 'Tiểu yêu PM2.5', 'parents': 'Bố mẹ Bắp'}[e]
        chars += f'<span class="chip var">{E(label)}</span>'
    return f'''
<article class="shot panel" id="shot-{x['id']}" data-chars="{' '.join(x['chars'])}">
  <header class="shot-head">
    <span class="shot-id">{x['id']}</span>
    <div class="shot-t"><b>Cảnh {x['sc']} · {E(SCENES[x['sc']-1]['title'])}</b><span>{x['tc']} · Tạo 10s · Dùng {x['use']}s</span></div>
  </header>
  <div class="scene-meta">
    <div><span class="lbl">Nhân vật xuất hiện</span><div class="chips">{chars}</div></div>
    <div><span class="lbl">Bối cảnh</span><div class="chips">{''.join(locchip(k) for k in x['loc'])}</div></div>
  </div>
  <p class="shot-vi">{E(x['vi'])}</p>
  <p class="shot-audio"><span class="lbl">Âm thanh</span>{E(x['audio'])}</p>
  <div class="prompt-box">
    <div class="pb-head"><span>Prompt Seedance 2.0 · 10s</span><button type="button" class="copy" data-copy="p-{x['id']}">Sao chép</button></div>
    <pre id="p-{x['id']}">{E(p)}</pre>
  </div>
</article>'''

filter_btns = '<button type="button" class="fbtn on" data-f="all">Tất cả</button>' + ''.join(f'<button type="button" class="fbtn" data-f="{k}"><i class="av av-{k}"></i>{E(CHARS[k]["name"])}</button>' for k in ORDER)
tab_prompt = f'''
<section class="panel intro">
  <h2>Prompt chi tiết Seedance 2.0</h2>
  <p>{len(SHOTS)} shot, mỗi shot tạo 10 giây. Cách dùng: tải 5 ảnh sheet theo thứ tự <b>@Image1 Bắp · @Image2 Na · @Image3 Su · @Image4 Cô giáo · @Image5 Mây Mây</b>. Nếu cần giữ bối cảnh, thêm ảnh bối cảnh (tab Bối cảnh) làm @Image6. Sau đó dán prompt của shot.</p>
  <div class="filters" role="group" aria-label="Lọc theo nhân vật">{filter_btns}</div>
  <p class="note" id="fcount">Đang hiện {len(SHOTS)} shot.</p>
</section>
{''.join(shot_card(x) for x in SHOTS)}
'''

# Tab 4: Bối cảnh
def loc_card(k, v):
    shots = [x['id'] for x in SHOTS if k in x['loc']]
    sws = ''.join(f'<span class="dot" style="background:{c}" title="{c}"></span>' for c in v['colors'])
    return f'''
<article class="locc panel" id="{k}">
  <header class="shot-head">
    <span class="shot-id">{k}</span>
    <div class="shot-t"><b>{E(v['name'])}</b><span>Cảnh {v['scenes']} · Shot {', '.join(shots)}</span></div>
    <div class="loc-sw">{sws}</div>
  </header>
  <dl class="locdl">
    <dt>Mô tả</dt><dd>{E(v['desc'])}</dd>
    <dt>Ánh sáng</dt><dd>{E(v['light'])}</dd>
  </dl>
  <div class="prompt-box">
    <div class="pb-head"><span>Prompt ảnh bối cảnh (không nhân vật)</span><button type="button" class="copy" data-copy="l-{k}">Sao chép</button></div>
    <pre id="l-{k}">{E(v['prompt'])}</pre>
  </div>
</article>'''

tab_loc = f'''
<section class="panel intro">
  <h2>Bối cảnh</h2>
  <p>10 bối cảnh dùng trong phim. Nên tạo ảnh bối cảnh trống (không nhân vật) bằng prompt bên dưới trước, rồi dùng làm ảnh tham chiếu @Image6 cho các shot cùng bối cảnh để giữ đồng nhất.</p>
</section>
{''.join(loc_card(k, v) for k, v in LOCS.items())}
'''

PAGE = f'''<title>Mây Mây Đi Lạc</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: fixed collage of the five character sheets behind a sky-tinted veil; content sits on frosted "cloud" panels under a sticky tab bar. */
:root {{
  --sky: #8FD3FF;
  --bg: #EAF5FD;
  --veil: rgba(234, 245, 253, .86);
  --panel: rgba(255, 255, 255, .9);
  --panel-2: #F3F8FC;
  --line: #D3E2EE;
  --fg: #1F2A55;
  --muted: #56627F;
  --accent: #F7C826;
  --accent-ink: #4A3A00;
  --link: #1F6FB2;
  --code-bg: #F6F9FC;
  --display: "Baloo 2", "Be Vietnam Pro", system-ui, sans-serif;
  --body: "Be Vietnam Pro", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #0F1A2E; --veil: rgba(13, 22, 40, .9); --panel: rgba(22, 34, 58, .92); --panel-2: #1B2A47; --line: #2C3D5E;
  --fg: #EAF2FB; --muted: #A9B7CF; --accent: #F7C826; --accent-ink: #2A2100; --link: #8FD3FF; --code-bg: #121E35; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #0F1A2E; --veil: rgba(13, 22, 40, .9); --panel: rgba(22, 34, 58, .92); --panel-2: #1B2A47; --line: #2C3D5E;
  --fg: #EAF2FB; --muted: #A9B7CF; --accent: #F7C826; --accent-ink: #2A2100; --link: #8FD3FF; --code-bg: #121E35; color-scheme: dark; }}
{css_imgs}
* {{ box-sizing: border-box; }}
[hidden] {{ display: none !important; }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 15px; line-height: 1.6; }}
.bgwall {{ position: fixed; inset: 0; z-index: 0; display: grid; grid-template-columns: repeat(3, 1fr); grid-auto-rows: 34vh; gap: 0; overflow: hidden; pointer-events: none; }}
.bgwall i {{ background-size: cover; background-position: center; }}
.bgwall::after {{ content: ""; position: absolute; inset: 0; background: var(--veil); }}
.wrap {{ position: relative; z-index: 1; max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 0 48px; }}
body::before {{ content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--panel); }}
.topbar {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; margin-inline: calc(-1 * max(16px, env(safe-area-inset-left, 0px))); padding: 10px max(16px, env(safe-area-inset-right, 0px)) 10px max(16px, env(safe-area-inset-left, 0px)); background: var(--panel); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }}
.brand {{ font-family: var(--display); font-weight: 800; font-size: 20px; display: flex; align-items: center; gap: 8px; }}
.brand i {{ width: 30px; height: 30px; border-radius: 50%; }}
.tabs {{ display: flex; gap: 4px; flex-wrap: wrap; margin-left: auto; }}
.tabs a {{ text-decoration: none; color: var(--muted); font-weight: 600; padding: 7px 14px; border-radius: 999px; font-size: 14px; }}
.tabs a:hover {{ color: var(--fg); background: var(--panel-2); }}
.tabs a[aria-current="page"] {{ background: var(--accent); color: var(--accent-ink); }}
a:focus-visible, button:focus-visible {{ outline: 3px solid var(--link); outline-offset: 2px; }}
main {{ display: grid; gap: 18px; padding-top: 20px; }}
.tab {{ display: grid; gap: 18px; }}
.panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 20px; padding: 22px; backdrop-filter: blur(8px); min-width: 0; }}
h1, h2, h3, h4 {{ font-family: var(--display); line-height: 1.15; text-wrap: balance; margin: 0; }}
h2 {{ font-size: 26px; font-weight: 800; }}
h3 {{ font-size: 20px; font-weight: 700; }}
h4 {{ font-size: 15px; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); font-family: var(--body); }}
.sub {{ margin-top: 24px; margin-bottom: 10px; }}
.note {{ color: var(--muted); margin: 6px 0 14px; max-width: 70ch; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .08em; font-size: 12px; font-weight: 600; color: var(--muted); margin: 0 0 6px; }}
.hero {{ display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); gap: 20px; align-items: center; padding: 30px; }}
.hero h1 {{ font-size: clamp(40px, 7vw, 68px); font-weight: 800; letter-spacing: -.01em; }}
.logline {{ font-size: 17px; max-width: 58ch; margin: 10px 0 16px; }}
.msg {{ margin: 0; padding: 12px 16px; border-radius: 14px; background: var(--panel-2); font-weight: 600; }}
.msg span {{ display: block; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); font-weight: 600; }}
.hero-cast {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }}
.hero-cast .av {{ aspect-ratio: 1; border-radius: 50%; border: 3px solid var(--panel); box-shadow: 0 4px 14px rgba(31, 42, 85, .15); }}
.hero-cast .big {{ grid-column: 1 / -1; aspect-ratio: 2.2; border-radius: 26px; background-size: 300% auto; background-position: 0% 45%; background-color: #8C8F96; }}
.av {{ display: inline-block; background-size: 300% auto; background-position: 0% 22%; background-repeat: no-repeat; background-color: #8C8F96; flex: none; }}
.av-may {{ background-position: 0% 40%; }}
.specs {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }}
.specs div {{ background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 14px 16px; display: grid; }}
.specs span, .lbl {{ font-size: 12px; text-transform: uppercase; letter-spacing: .07em; color: var(--muted); font-weight: 600; }}
.specs b {{ font-family: var(--display); font-size: 22px; font-weight: 700; }}
.specs small {{ color: var(--muted); }}
.timeline {{ display: flex; gap: 3px; height: 46px; border-radius: 12px; overflow: hidden; }}
.tl-seg {{ display: grid; place-items: center; text-decoration: none; color: var(--accent-ink); background: var(--accent); font-family: var(--display); font-size: 17px; min-width: 0; }}
.tl-seg:nth-child(2n) {{ background: var(--sky); color: #10324F; }}
.tl-seg:nth-child(2), .tl-seg:nth-child(5) {{ background: #8A8D91; color: #fff; }}
.tl-seg:hover {{ filter: brightness(1.08); }}
.tl-scale {{ display: flex; justify-content: space-between; color: var(--muted); font-size: 12px; margin-top: 6px; font-variant-numeric: tabular-nums; }}
.chars {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 14px; }}
.char {{ border: 1px solid var(--line); border-radius: 16px; overflow: hidden; background: var(--panel-2); display: grid; grid-template-rows: auto 1fr; }}
.sheet {{ aspect-ratio: 16 / 9; background-size: cover; background-position: center; max-width: 100%; }}
.char-body {{ padding: 14px 16px 16px; }}
.char-body header {{ display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }}
.ref {{ font-family: var(--mono); font-size: 12px; background: var(--accent); color: var(--accent-ink); padding: 2px 8px; border-radius: 6px; }}
.role {{ margin: 2px 0 8px; color: var(--muted); font-size: 13px; }}
dl {{ margin: 0; display: grid; gap: 4px; }}
dt {{ font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); font-weight: 600; margin-top: 6px; }}
dd {{ margin: 0; }}
.extras {{ list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; }}
.extras li {{ border: 1px dashed var(--line); border-radius: 14px; padding: 12px 14px; display: grid; gap: 2px; }}
.extras span {{ color: var(--muted); font-size: 14px; }}
.lock-head {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
.lock-badge {{ display: inline-flex; align-items: center; gap: 6px; font-weight: 700; font-size: 13px; padding: 4px 12px; border-radius: 999px; background: var(--fg); color: var(--bg); }}
.lock-badge svg {{ width: 14px; height: 14px; fill: currentColor; }}
.pals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }}
.pal h4 {{ margin-bottom: 8px; }}
.sws {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 6px; }}
.sw {{ display: flex; align-items: center; gap: 10px; }}
.dot {{ width: 34px; height: 34px; border-radius: 10px; border: 1px solid var(--line); flex: none; display: inline-block; }}
.sw-t {{ display: grid; grid-template-columns: auto auto; column-gap: 8px; align-items: baseline; justify-content: start; }}
.sw-t code {{ font-family: var(--mono); font-size: 12px; color: var(--muted); }}
.sw-t small {{ grid-column: 1 / -1; color: var(--muted); font-size: 12px; }}
.cscript {{ list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)); gap: 10px; }}
.cscript li {{ display: grid; gap: 2px; font-size: 13px; }}
.cs-bar {{ height: 54px; border-radius: 10px; border: 1px solid var(--line); }}
.cscript small {{ color: var(--muted); font-size: 12px; line-height: 1.35; }}
.rules {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }}
.rules li {{ padding: 10px 14px; background: var(--panel-2); border-radius: 12px; }}
.rules b {{ display: inline-block; min-width: 9.5em; }}
.prompt-box {{ margin-top: 14px; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; background: var(--code-bg); }}
.pb-head {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--line); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); font-weight: 600; }}
.copy {{ font: inherit; text-transform: none; letter-spacing: 0; font-size: 13px; font-weight: 600; border: 0; border-radius: 8px; padding: 5px 12px; background: var(--accent); color: var(--accent-ink); cursor: pointer; }}
.copy.done {{ background: #7CC66B; color: #0F3010; }}
pre {{ margin: 0; padding: 12px 14px; font-family: var(--mono); font-size: 12.5px; line-height: 1.55; white-space: pre-wrap; word-break: break-word; max-height: 360px; overflow: auto; }}
.intro p {{ max-width: 75ch; }}
.acts {{ list-style: none; padding: 0; margin: 14px 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
.acts li {{ padding: 12px 14px; border-radius: 14px; background: var(--panel-2); display: grid; }}
.acts span {{ color: var(--muted); font-size: 13px; }}
.scene-head, .shot-head {{ display: flex; gap: 14px; align-items: center; flex-wrap: wrap; }}
.scene-n, .shot-id {{ font-family: var(--display); font-weight: 800; font-size: 22px; min-width: 52px; height: 52px; padding: 0 10px; border-radius: 16px; display: grid; place-items: center; background: var(--accent); color: var(--accent-ink); }}
.tc {{ margin: 2px 0 0; color: var(--muted); font-variant-numeric: tabular-nums; }}
.tc a, .shot-t a {{ color: var(--link); }}
.shot-t {{ display: grid; min-width: 0; flex: 1; }}
.shot-t span {{ color: var(--muted); font-size: 13px; font-variant-numeric: tabular-nums; }}
.scene-meta {{ display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 14px; margin-top: 14px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }}
.chip {{ display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px 3px 3px; border-radius: 999px; background: var(--panel-2); border: 1px solid var(--line); font-size: 13px; font-weight: 600; color: var(--fg); text-decoration: none; }}
.chip .av {{ width: 24px; height: 24px; border-radius: 50%; }}
.chip b {{ font-family: var(--mono); font-weight: 500; font-size: 11px; color: var(--muted); }}
.chip.var {{ padding: 3px 10px; border-style: dashed; }}
.chip.loc {{ padding: 3px 10px 3px 3px; }}
.chip.loc:hover {{ border-color: var(--link); }}
.loc-id {{ font-family: var(--mono); font-size: 11px; background: var(--fg); color: var(--bg); padding: 2px 6px; border-radius: 999px; }}
.none {{ color: var(--muted); font-size: 13px; }}
.scene-cols {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 18px; margin-top: 16px; }}
.col p {{ margin: 6px 0; }}
.snd {{ list-style: none; padding: 0; margin: 6px 0 0; display: grid; gap: 6px; }}
.snd li {{ display: grid; grid-template-columns: 8.5em minmax(0, 1fr); gap: 8px; }}
.snd b {{ color: var(--link); font-size: 14px; }}
.shot-vi {{ margin: 12px 0 4px; font-weight: 500; }}
.shot-audio {{ margin: 0; color: var(--muted); font-size: 14px; }}
.shot-audio .lbl {{ margin-right: 8px; }}
.filters {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }}
.fbtn {{ font: inherit; font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 999px; border: 1px solid var(--line); background: var(--panel-2); color: var(--fg); cursor: pointer; }}
.fbtn .av {{ width: 22px; height: 22px; border-radius: 50%; margin-left: -8px; }}
.fbtn.on {{ background: var(--fg); color: var(--bg); border-color: var(--fg); }}
.loc-sw {{ display: flex; gap: 4px; margin-left: auto; }}
.loc-sw .dot {{ width: 22px; height: 22px; border-radius: 6px; }}
.locdl {{ margin-top: 12px; }}
.flash {{ animation: flash 1.4s ease; }}
@keyframes flash {{ 0%, 40% {{ box-shadow: 0 0 0 4px var(--accent); }} 100% {{ box-shadow: 0 0 0 0 transparent; }} }}
@media (prefers-reduced-motion: reduce) {{ .flash {{ animation: none; }} }}
@media (max-width: 760px) {{
  .hero {{ grid-template-columns: 1fr; padding: 20px; }}
  .scene-meta, .scene-cols {{ grid-template-columns: 1fr; }}
  .tabs {{ margin-left: 0; width: 100%; overflow-x: auto; flex-wrap: nowrap; }}
  .tabs a {{ white-space: nowrap; }}
  .panel {{ padding: 16px; }}
  .snd li {{ grid-template-columns: 1fr; gap: 0; }}
  .rules b {{ display: block; }}
  .loc-sw {{ margin-left: 0; }}
  .bgwall {{ grid-template-columns: repeat(2, 1fr); grid-auto-rows: 22vh; }}
}}
</style>

<div class="bgwall" aria-hidden="true">
  <i class="av-bap"></i><i class="av-may"></i><i class="av-na"></i>
  <i class="av-su"></i><i class="av-co"></i><i class="av-bap"></i>
  <i class="av-may"></i><i class="av-na"></i><i class="av-su"></i>
</div>

<div class="wrap">
  <div class="topbar">
    <div class="brand"><i class="av av-may"></i>Mây Mây Đi Lạc</div>
    <nav class="tabs" aria-label="Các tab kịch bản">
      <a href="#tong-quan" data-tab="tong-quan">Tổng quan</a>
      <a href="#noi-dung" data-tab="noi-dung">Nội dung</a>
      <a href="#prompt" data-tab="prompt">Prompt chi tiết</a>
      <a href="#boi-canh" data-tab="boi-canh">Bối cảnh</a>
    </nav>
  </div>
  <main>
    <div class="tab" id="tab-tong-quan">{tab_overview}</div>
    <div class="tab" id="tab-noi-dung" hidden>{tab_content}</div>
    <div class="tab" id="tab-prompt" hidden>{tab_prompt}</div>
    <div class="tab" id="tab-boi-canh" hidden>{tab_loc}</div>
  </main>
</div>

<script>
(function () {{
  var TABS = ['tong-quan', 'noi-dung', 'prompt', 'boi-canh'];
  function show(name, target) {{
    if (TABS.indexOf(name) < 0) name = 'tong-quan';
    TABS.forEach(function (t) {{ document.getElementById('tab-' + t).hidden = t !== name; }});
    document.querySelectorAll('.tabs a').forEach(function (a) {{
      if (a.dataset.tab === name) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    }});
    if (target) {{
      var el = document.getElementById(target);
      if (el) {{ el.scrollIntoView({{ behavior: 'smooth', block: 'start' }}); el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); return; }}
    }}
    window.scrollTo(0, 0);
  }}
  var pending = null;
  document.addEventListener('click', function (e) {{
    var g = e.target.closest('[data-goto]');
    if (g) pending = g.dataset.goto;
  }}, true);
  window.addEventListener('hashchange', function () {{ show(location.hash.slice(1), pending); pending = null; }});
  document.querySelectorAll('[data-goto]').forEach(function (a) {{
    a.addEventListener('click', function (e) {{
      if (a.getAttribute('href') === location.hash) {{ e.preventDefault(); show(location.hash.slice(1), a.dataset.goto); pending = null; }}
    }});
  }});
  show(location.hash.slice(1));

  document.addEventListener('click', function (e) {{
    var b = e.target.closest('.copy'); if (!b) return;
    var pre = document.getElementById(b.dataset.copy); var text = pre.textContent;
    function ok() {{ b.textContent = 'Đã sao chép'; b.classList.add('done'); setTimeout(function () {{ b.textContent = 'Sao chép'; b.classList.remove('done'); }}, 1600); }}
    function fallback() {{ var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Đã chọn, nhấn Ctrl+C'; }}
    try {{ navigator.clipboard.writeText(text).then(ok, fallback); }} catch (err) {{ fallback(); }}
  }});

  var btns = document.querySelectorAll('.fbtn'), shots = document.querySelectorAll('.shot'), count = document.getElementById('fcount');
  btns.forEach(function (b) {{
    b.addEventListener('click', function () {{
      btns.forEach(function (x) {{ x.classList.toggle('on', x === b); }});
      var f = b.dataset.f, n = 0;
      shots.forEach(function (s) {{ var on = f === 'all' || s.dataset.chars.split(' ').indexOf(f) >= 0; s.hidden = !on; if (on) n++; }});
      count.textContent = 'Đang hiện ' + n + ' shot.';
    }});
  }});
}})();
</script>
'''

OUT.write_text(PAGE, encoding='utf-8')
print('written', OUT, round(OUT.stat().st_size / 1024), 'KB', 'shots', len(SHOTS), 'used', total_used)
