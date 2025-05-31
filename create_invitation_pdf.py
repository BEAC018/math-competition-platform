#!/usr/bin/env python3
"""
إنشاء دعوة PDF للمشاركين
Create PDF invitation for participants
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_invitation_pdf():
    """إنشاء ملف PDF للدعوة"""
    
    # إنشاء ملف PDF
    doc = SimpleDocTemplate("دعوة_المسابقة_الرياضية.pdf", pagesize=A4,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # قائمة العناصر
    story = []
    
    # الأنماط
    styles = getSampleStyleSheet()
    
    # نمط العنوان الرئيسي
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # وسط
        textColor=colors.HexColor('#1976D2')
    )
    
    # نمط العنوان الفرعي
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        alignment=1,
        textColor=colors.HexColor('#4FC3F7')
    )
    
    # نمط النص العادي
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=0,  # يسار
        textColor=colors.black
    )
    
    # نمط الرابط
    link_style = ParagraphStyle(
        'CustomLink',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=15,
        alignment=1,
        textColor=colors.HexColor('#1976D2'),
        backColor=colors.HexColor('#E3F2FD')
    )
    
    # العنوان الرئيسي
    story.append(Paragraph("🎯 منصة المسابقات الرياضية التفاعلية", title_style))
    story.append(Spacer(1, 12))
    
    # العنوان الفرعي
    story.append(Paragraph("اختبر قدراتك الحسابية واستمتع بالتعلم!", subtitle_style))
    story.append(Spacer(1, 20))
    
    # الرابط المباشر
    story.append(Paragraph("🌐 الرابط المباشر للمنصة:", subtitle_style))
    story.append(Paragraph("https://ecf1-105-157-119-224.ngrok-free.app/student/login/", link_style))
    story.append(Spacer(1, 20))
    
    # رمز الدخول
    story.append(Paragraph("🔑 رمز الدخول: <b>ben25</b>", subtitle_style))
    story.append(Spacer(1, 20))
    
    # خطوات الدخول
    story.append(Paragraph("📝 خطوات الدخول:", subtitle_style))
    
    steps_data = [
        ["1️⃣", "انقر على الرابط أعلاه"],
        ["2️⃣", "اكتب اسمك الكامل"],
        ["3️⃣", "اكتب رمز الدخول: ben25"],
        ["4️⃣", "اختر مستواك الدراسي (1-9)"],
        ["5️⃣", "ابدأ المسابقة واستمتع!"]
    ]
    
    steps_table = Table(steps_data, colWidths=[1*inch, 4*inch])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0'))
    ]))
    
    story.append(steps_table)
    story.append(Spacer(1, 20))
    
    # مميزات المنصة
    story.append(Paragraph("🎮 مميزات المنصة:", subtitle_style))
    
    features_data = [
        ["⏱️ توقيت سريع", "10-15 ثانية لكل سؤال"],
        ["📊 9 مستويات", "صعوبة متدرجة ومناسبة"],
        ["🧮 عمليات متنوعة", "جمع، طرح، ضرب، قسمة"],
        ["📈 نتائج فورية", "تقييم مباشر للأداء"],
        ["🏆 تحليل الأداء", "نقاط القوة والضعف"],
        ["📱 متوافق مع الجوال", "يعمل على جميع الأجهزة"]
    ]
    
    features_table = Table(features_data, colWidths=[2*inch, 3*inch])
    features_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BBDEFB'))
    ]))
    
    story.append(features_table)
    story.append(Spacer(1, 20))
    
    # نصائح للنجاح
    story.append(Paragraph("💡 نصائح للنجاح:", subtitle_style))
    
    tips = [
        "• تأكد من اتصال الإنترنت",
        "• استخدم بيئة هادئة للتركيز",
        "• اقرأ السؤال بعناية قبل الإجابة",
        "• لا تتردد في المحاولة مرة أخرى"
    ]
    
    for tip in tips:
        story.append(Paragraph(tip, normal_style))
    
    story.append(Spacer(1, 30))
    
    # الخاتمة
    story.append(Paragraph("🎯 استمتعوا بالتعلم والمنافسة!", subtitle_style))
    story.append(Paragraph("تم تطوير هذه المنصة خصيصاً لتحسين مهاراتكم الحسابية", normal_style))
    
    # بناء PDF
    doc.build(story)
    print("✅ تم إنشاء ملف دعوة_المسابقة_الرياضية.pdf")

def create_qr_code():
    """إنشاء QR Code للرابط"""
    try:
        import qrcode
        from PIL import Image
        
        # إنشاء QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data("https://ecf1-105-157-119-224.ngrok-free.app/student/login/")
        qr.make(fit=True)
        
        # إنشاء الصورة
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qr_code_منصة_المسابقة.png")
        
        print("✅ تم إنشاء QR Code: qr_code_منصة_المسابقة.png")
        
    except ImportError:
        print("⚠️ لإنشاء QR Code، قم بتثبيت: pip install qrcode[pil]")

def main():
    """الدالة الرئيسية"""
    print("📄 إنشاء مواد الدعوة للمشاركين...")
    
    # إنشاء PDF
    create_invitation_pdf()
    
    # إنشاء QR Code
    create_qr_code()
    
    print("\n🎉 تم إنشاء جميع مواد الدعوة بنجاح!")
    print("📁 الملفات المنشأة:")
    print("   • دعوة_المسابقة_الرياضية.pdf")
    print("   • qr_code_منصة_المسابقة.png")
    print("   • invitation_email.html")

if __name__ == "__main__":
    main()
