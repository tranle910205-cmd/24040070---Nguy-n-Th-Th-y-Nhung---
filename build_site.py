from pathlib import Path
import html, re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
NAV = [('index.html','Trang chủ'),('business-plan.html','Kế hoạch kinh doanh'),('financial-analysis.html','Phân tích tài chính'),('swot.html','Phân tích SWOT'),('five-forces.html','5 áp lực cạnh tranh'),('reflections.html','Phản hồi đọc sách'),('action-plan.html','Hành động 90 ngày')]
E = html.escape

def page(file, title, intro, body, eyebrow='HỒ SƠ DỰ ÁN'):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url==file or (file.startswith('reflection-') and url=='reflections.html') else '')+f'><span>{i:02}</span>{label}</a>' for i,(url,label) in enumerate(NAV,1))
    doc = f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{E(intro)}"><title>{E(title)} · Hồ sơ khởi nghiệp</title><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">Đến nội dung chính</a><aside class="sidebar"><a class="brand" href="index.html"><b class="brandmark">↗</b><span>HỒ SƠ<br><strong>KHỞI NGHIỆP</strong></span></a><p class="nav-label">KHÁM PHÁ DỰ ÁN</p><nav aria-label="Điều hướng chính">{nav}</nav><div class="side-note"><span class="dot"></span> Nội dung từ Markdown<p>Kế hoạch · Phân tích · Góc nhìn thành viên</p></div></aside>
<div class="workspace"><header class="topbar"><span>Hồ sơ dự án <span class="muted">/ {E(title)}</span></span><a href="reflections.html">Góc đọc sách ↗</a></header><main id="main"><div class="page-heading"><p class="eyebrow">{eyebrow}</p><h1>{E(title)}</h1><p class="lead">{E(intro)}</p></div>{body}</main><footer><span>HỒ SƠ KHỞI NGHIỆP</span><span>Nội dung được trình bày theo tài liệu nguồn.</span><a href="#main">Lên đầu trang ↑</a></footer></div></body></html>'''
    (ROOT/file).write_text(doc, encoding='utf-8')

def notice():
    return '<div class="notice"><strong>Chưa có nguồn kế hoạch kinh doanh</strong><p>Chưa tìm thấy <code>business_plan.md</code> trong dự án. Nội dung kinh doanh sẽ được bổ sung khi có tài liệu chính thức.</p></div>'

summaries = {
'Nguyễn Thị Dịu Hiền': ('Co-Intelligence – Trí Tuệ Đồng Hành', 'Nhìn AI như một cộng sự để phát triển ý tưởng và tư duy. Bài phản hồi nhấn mạnh việc kiểm chứng thông tin, giữ sự chủ động và chịu trách nhiệm khi sử dụng AI.', 'Đồng hành cùng AI'),
'Nguyễn Thị Thùy Nhung': ('Siêu Trí Tuệ', 'Từ vấn đề kiểm soát siêu trí tuệ và căn chỉnh giá trị, thành viên rút ra bài học về đạo đức, tư duy độc lập và sự chuẩn bị dài hạn trước những thay đổi công nghệ.', 'Kiểm soát & giá trị'),
'Quách Ngọc Minh': ('Bản Đồ AI: Quyền Lực, Chính Trị và Sự Tiêu Tốn Tài Nguyên của Hành Tinh', 'Bài phản hồi mở rộng góc nhìn về tài nguyên, lao động, dữ liệu và quyền lực phía sau AI; nhấn mạnh tư duy phản biện, quyền riêng tư và trách nhiệm khi sử dụng công nghệ.', 'Công nghệ & trách nhiệm'),
'Trần Thụy Bảo Ngọc': ('Siêu Trí Tuệ', 'Suy ngẫm về mục tiêu và khả năng kiểm soát AI, thành viên nhấn mạnh rằng công nghệ cần được định hướng bằng trách nhiệm, đồng thời người dùng phải giữ khả năng kiểm chứng và tự đánh giá.', 'Con người & định hướng')}

def inline(text):
    text = E(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)

def markdown(text):
    out=[]
    for block in re.split(r'\n\s*\n', text.strip()):
        if re.fullmatch(r'#\s+\d+',block.strip()):
            continue # Student identifiers are not displayed.
        lines=block.splitlines()
        if block.startswith('#'):
            m=re.match(r'^(#{1,6})\s+(.*)',block,re.S)
            level=min(4,len(m[1])+1)
            out.append(f'<h{level}>{inline(m[2])}</h{level}>')
        elif all(re.match(r'^[-*] ',l) for l in lines):
            out.append('<ul>'+''.join('<li>'+inline(l[2:])+'</li>' for l in lines)+'</ul>')
        elif all(re.match(r'^\d+\. ',l) for l in lines):
            out.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',l))+'</li>' for l in lines)+'</ol>')
        elif re.fullmatch(r'\*\*\d+\..*\*\*',block,re.S):
            out.append('<h2>'+inline(block)+'</h2>')
        else:
            out.append('<p>'+inline(block).replace('\n','<br>')+'</p>')
    return '\n'.join(out)

cards=[]
for n,source in enumerate(sorted((ROOT/'Reflections').glob('*.md')),1):
    text=source.read_text(encoding='utf-8-sig')
    name=re.search(r'Họ Và Tên:\s*(.+)',text)[1].strip()
    book,summary,tag=summaries[name]
    file=f'reflection-{n:02}.html'
    source_url=quote(source.relative_to(ROOT).as_posix())
    cards.append(f'<article class="card member"><div class="card-top"><span class="avatar">{E("".join(x[0] for x in name.split()[-2:]))}</span><span class="tag">{tag}</span></div><h2>{E(name)}</h2><p class="book">{E(book)}</p><p>{E(summary)}</p><a class="text-link" href="{file}">Đọc bài phản hồi <span>↗</span></a></article>')
    body=f'<a class="back" href="reflections.html">← Tất cả bài phản hồi</a><div class="article-layout"><article class="prose">{markdown(text)}</article><aside class="reading-note"><p class="eyebrow">TÀI LIỆU GỐC</p><h2>{E(book)}</h2><p>Bài phản hồi của {E(name)}.</p><a class="button secondary" href="{source_url}">Mở tệp Markdown ↗</a><p class="small">Nội dung bài được giữ riêng theo đúng tệp nguồn. Mã số sinh viên không hiển thị trong bài.</p></aside></div>'
    page(file,name,book,body,'GÓC NHÌN THÀNH VIÊN')

page('reflections.html','Phản hồi đọc sách','Những góc nhìn riêng về trí tuệ nhân tạo, con người và trách nhiệm với công nghệ.', '<div class="section-heading"><h2>Mỗi thành viên, một góc nhìn</h2><span class="tag">Bài phản hồi cá nhân</span></div><div class="grid two">'+''.join(cards)+'</div>','THƯ VIỆN GÓC NHÌN')

explore=''.join(f'<a class="card explore" href="{f}"><span class="eyebrow">{i:02}</span><h3>{label}</h3><span class="arrow">↗</span></a>' for i,(f,label) in enumerate(NAV[1:],1))
page('index.html','Tổng quan dự án','Không gian kết nối kế hoạch kinh doanh, phân tích chiến lược và những góc nhìn của thành viên.', '<section class="hero"><div><span class="pill">HỒ SƠ KHỞI NGHIỆP</span><h2>Từ ý tưởng<br>đến hành động.</h2><p>Khám phá hồ sơ dự án và những suy ngẫm từ hành trình đọc sách của từng thành viên.</p><a class="button" href="reflections.html">Khám phá góc đọc sách ↗</a></div><div class="hero-art" aria-hidden="true"><div class="orbit"></div><span class="art-word">Ý TƯỞNG</span><b>↗</b><span class="art-bottom">TƯ DUY · CHIẾN LƯỢC · HÀNH ĐỘNG</span></div></section>'+notice()+'<section><div class="section-heading"><h2>Khám phá hồ sơ</h2><span class="muted">Các chuyên mục dự án</span></div><div class="grid three">'+explore+'</div></section><section><div class="section-heading"><h2>Góc nhìn thành viên</h2><a class="text-link" href="reflections.html">Tất cả bài phản hồi ↗</a></div><div class="grid two">'+''.join(cards[:2])+'</div></section>')

page('business-plan.html','Kế hoạch kinh doanh','Tài liệu nền tảng cho định hướng và toàn bộ nội dung kinh doanh của dự án.',notice()+'<section class="empty"><span class="empty-icon">↗</span><h2>Đang chờ kế hoạch chính thức</h2><p>Các tệp hiện có trong Business-plan/Thành Viên là bài phản hồi đọc sách, không phải kế hoạch kinh doanh.</p><a class="button secondary" href="reflections.html">Xem bài phản hồi thành viên ↗</a></section>')

page('financial-analysis.html','Phân tích tài chính','Các chỉ số và trực quan hóa tài chính theo kế hoạch kinh doanh chính thức.',notice()+'<section class="card financial-empty"><p class="eyebrow">CHỈ SỐ TÀI CHÍNH</p><h2>Chưa có số liệu để trình bày</h2><p>Không có KPI hoặc biểu đồ tài chính khi chưa có dữ liệu từ business_plan.md.</p><div class="data-state">Dữ liệu nguồn đang thiếu</div></section>')

swot=[('S','Điểm mạnh','Strengths'),('W','Điểm yếu','Weaknesses'),('O','Cơ hội','Opportunities'),('T','Thách thức','Threats')]
page('swot.html','Phân tích SWOT','Bốn góc nhìn chiến lược được trình bày tách biệt theo nội dung nguồn.',notice()+'<div class="grid two swot">'+''.join(f'<article class="card"><span class="swot-letter">{letter}</span><p class="eyebrow">{eng}</p><h2>{title}</h2><p>Chưa có nội dung từ kế hoạch kinh doanh chính thức.</p></article>' for letter,title,eng in swot)+'</div>')

forces=['Mức độ cạnh tranh trong ngành','Nguy cơ từ đối thủ mới gia nhập','Quyền thương lượng của nhà cung cấp','Quyền thương lượng của khách hàng','Nguy cơ từ sản phẩm hoặc dịch vụ thay thế']
page('five-forces.html','5 áp lực cạnh tranh của Porter','Tách riêng từng yếu tố để theo dõi cấu trúc cạnh tranh của dự án.',notice()+'<div class="grid two forces">'+''.join(f'<article class="card"><div class="card-top"><span class="force-number">{i:02}</span><span class="tag neutral">Chưa có nội dung nguồn</span></div><h2>{title}</h2><p>Chưa có phân tích từ business_plan.md để trình bày yếu tố này.</p></article>' for i,title in enumerate(forces,1))+'</div><p class="source-note">Các số thứ tự chỉ dùng để phân biệt năm yếu tố, không phải điểm đánh giá. Chưa hiển thị mức định tính vì thiếu nguồn chính thức.</p>')

page('action-plan.html','Kế hoạch hành động 90 ngày','Lộ trình thực hiện theo các giai đoạn và mốc được xác định trong kế hoạch kinh doanh.',notice()+'<section class="card timeline-empty"><span class="timeline-dot"></span><p class="eyebrow">LỘ TRÌNH THỰC HIỆN</p><h2>Chưa có mốc hành động từ nguồn</h2><p>Timeline sẽ được trình bày khi có giai đoạn, công việc và thời hạn trong business_plan.md. Hiện chưa đặt mốc hoặc phân công nhiệm vụ.</p></section>')
print('Generated 11 HTML pages from the available sources.')
