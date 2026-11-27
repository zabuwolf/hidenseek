// =============================================================================
//  TRỐN TÌM — bộ vẽ ảnh tự động (System.Drawing). Chạy: tools\gen_art.ps1
//  Sinh ra: game/images/bg, game/images/char, game/images/items, game/images/fx, game/gui
// =============================================================================
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Drawing.Text;
using System.IO;
using System.Runtime.InteropServices;

public static class Art
{
    static string Root;
    const int W = 1920, H = 1080;
    static readonly Color OL = Color.FromArgb(220, 43, 29, 23);   // viền nét
    static HashSet<string> fonts;

    // ------------------------------------------------------------------ utils
    public static Color C(string hex) { return C(hex, 255); }
    public static Color C(string hex, int a)
    {
        hex = hex.TrimStart('#');
        return Color.FromArgb(a, Convert.ToInt32(hex.Substring(0, 2), 16),
            Convert.ToInt32(hex.Substring(2, 2), 16), Convert.ToInt32(hex.Substring(4, 2), 16));
    }
    static Color A(Color c, int a) { return Color.FromArgb(Math.Max(0, Math.Min(255, a)), c.R, c.G, c.B); }
    static Color N(bool night, string n, string d) { return night ? C(n) : C(d); }

    static Bitmap NB(int w, int h) { return new Bitmap(w, h, PixelFormat.Format32bppArgb); }
    static Graphics G(Bitmap b)
    {
        Graphics g = Graphics.FromImage(b);
        g.SmoothingMode = SmoothingMode.AntiAlias;
        g.InterpolationMode = InterpolationMode.HighQualityBicubic;
        g.PixelOffsetMode = PixelOffsetMode.HighQuality;
        g.CompositingQuality = CompositingQuality.HighQuality;
        g.TextRenderingHint = TextRenderingHint.AntiAliasGridFit;
        return g;
    }
    static void Save(Bitmap b, string rel)
    {
        string p = Path.Combine(Root, rel.Replace('/', '\\'));
        Directory.CreateDirectory(Path.GetDirectoryName(p));
        b.Save(p, ImageFormat.Png);
        Console.WriteLine("  " + rel);
    }
    static string F(string name)
    {
        if (fonts == null)
        {
            fonts = new HashSet<string>();
            foreach (FontFamily f in new InstalledFontCollection().Families) fonts.Add(f.Name);
        }
        return fonts.Contains(name) ? name : "Segoe UI";
    }

    static void Rect(Graphics g, Color c, float x, float y, float w, float h)
    { using (var br = new SolidBrush(c)) g.FillRectangle(br, x, y, w, h); }
    static void VGrad(Graphics g, float x, float y, float w, float h, Color a, Color b)
    { using (var br = new LinearGradientBrush(new RectangleF(x, y - 1, w, h + 2), a, b, 90f)) g.FillRectangle(br, x, y, w, h); }
    static void HGrad(Graphics g, float x, float y, float w, float h, Color a, Color b)
    { using (var br = new LinearGradientBrush(new RectangleF(x - 1, y, w + 2, h), a, b, 0f)) g.FillRectangle(br, x, y, w, h); }
    static void Ell(Graphics g, Color c, float cx, float cy, float rx, float ry)
    { using (var br = new SolidBrush(c)) g.FillEllipse(br, cx - rx, cy - ry, rx * 2, ry * 2); }
    static void EllO(Graphics g, Color c, Color o, float lw, float cx, float cy, float rx, float ry)
    {
        Ell(g, c, cx, cy, rx, ry);
        using (var p = new Pen(o, lw)) g.DrawEllipse(p, cx - rx, cy - ry, rx * 2, ry * 2);
    }
    static void Glow(Graphics g, float cx, float cy, float rx, float ry, Color c)
    {
        using (var p = new GraphicsPath())
        {
            p.AddEllipse(cx - rx, cy - ry, rx * 2, ry * 2);
            using (var pb = new PathGradientBrush(p))
            {
                pb.CenterPoint = new PointF(cx, cy);
                pb.CenterColor = c;
                pb.SurroundColors = new Color[] { A(c, 0) };
                var bl = new Blend();
                bl.Factors = new float[] { 0f, 0.18f, 0.55f, 1f };
                bl.Positions = new float[] { 0f, 0.35f, 0.72f, 1f };
                pb.Blend = bl;
                g.FillPath(pb, p);
            }
        }
    }
    static GraphicsPath RR(float x, float y, float w, float h, float r)
    {
        var p = new GraphicsPath();
        float d = r * 2; if (d > w) d = w; if (d > h) d = h;
        if (d < 1) { p.AddRectangle(new RectangleF(x, y, w, h)); return p; }
        p.AddArc(x, y, d, d, 180, 90); p.AddArc(x + w - d, y, d, d, 270, 90);
        p.AddArc(x + w - d, y + h - d, d, d, 0, 90); p.AddArc(x, y + h - d, d, d, 90, 90);
        p.CloseFigure(); return p;
    }
    static void FillRR(Graphics g, Color c, float x, float y, float w, float h, float r)
    { using (var p = RR(x, y, w, h, r)) using (var br = new SolidBrush(c)) g.FillPath(br, p); }
    static void FillRRO(Graphics g, Color c, Color o, float lw, float x, float y, float w, float h, float r)
    {
        using (var p = RR(x, y, w, h, r))
        {
            using (var br = new SolidBrush(c)) g.FillPath(br, p);
            using (var pen = new Pen(o, lw)) g.DrawPath(pen, p);
        }
    }
    static void StrokeRR(Graphics g, Color o, float lw, float x, float y, float w, float h, float r)
    { using (var p = RR(x, y, w, h, r)) using (var pen = new Pen(o, lw)) g.DrawPath(pen, p); }
    static PointF[] Pts(float[] a)
    {
        var r = new PointF[a.Length / 2];
        for (int i = 0; i < r.Length; i++) r[i] = new PointF(a[i * 2], a[i * 2 + 1]);
        return r;
    }
    static void Poly(Graphics g, Color c, params float[] pts)
    { using (var br = new SolidBrush(c)) g.FillPolygon(br, Pts(pts)); }
    static void PolyO(Graphics g, Color c, Color o, float lw, params float[] pts)
    {
        var p = Pts(pts);
        using (var br = new SolidBrush(c)) g.FillPolygon(br, p);
        using (var pen = new Pen(o, lw)) { pen.LineJoin = LineJoin.Round; g.DrawPolygon(pen, p); }
    }
    static Pen RP(Color c, float w)
    {
        var p = new Pen(c, w); p.StartCap = LineCap.Round; p.EndCap = LineCap.Round; p.LineJoin = LineJoin.Round; return p;
    }
    static void Ln(Graphics g, Color c, float w, float x1, float y1, float x2, float y2)
    { using (var p = RP(c, w)) g.DrawLine(p, x1, y1, x2, y2); }
    static void Arc(Graphics g, Color c, float w, float x, float y, float ww, float hh, float a0, float sw)
    { using (var p = RP(c, w)) g.DrawArc(p, x, y, ww, hh, a0, sw); }
    static void Bez(Graphics g, Color c, float w, float x1, float y1, float x2, float y2, float x3, float y3, float x4, float y4)
    { using (var p = RP(c, w)) g.DrawBezier(p, x1, y1, x2, y2, x3, y3, x4, y4); }
    static void Txt(Graphics g, string s, string font, float size, FontStyle st, Color c, float x, float y, bool center)
    {
        using (var f = new Font(F(font), size, st, GraphicsUnit.Pixel))
        using (var br = new SolidBrush(c))
        {
            if (center) { var sf = new StringFormat(); sf.Alignment = StringAlignment.Center; g.DrawString(s, f, br, x, y, sf); }
            else g.DrawString(s, f, br, x, y);
        }
    }
    static void Stars(Graphics g, int n, float w, float h, int seed)
    {
        var r = new Random(seed);
        for (int i = 0; i < n; i++)
        {
            float x = (float)r.NextDouble() * w, y = (float)r.NextDouble() * h;
            int a = 60 + r.Next(170);
            float s = r.Next(10) == 0 ? 2.2f : 1.2f;
            Ell(g, Color.FromArgb(a, 230, 235, 255), x, y, s, s);
        }
    }
    static void Grain(Graphics g, int w, int h, int n, int alpha, int seed)
    {
        var r = new Random(seed);
        using (var bl = new SolidBrush(Color.FromArgb(alpha, 0, 0, 0)))
        using (var wh = new SolidBrush(Color.FromArgb(alpha / 5, 255, 255, 255)))
            for (int i = 0; i < n / 2; i++)
                g.FillRectangle(r.Next(4) == 0 ? wh : bl, r.Next(w), r.Next(h), 1.5f, 1.5f);
    }
    static void Vignette(Graphics g, int w, int h, int alpha)
    {
        using (var p = new GraphicsPath())
        {
            p.AddEllipse(-w * 0.25f, -h * 0.3f, w * 1.5f, h * 1.6f);
            using (var pb = new PathGradientBrush(p))
            {
                pb.CenterPoint = new PointF(w / 2f, h / 2f);
                pb.CenterColor = Color.FromArgb(0, 0, 0, 0);
                pb.SurroundColors = new Color[] { Color.FromArgb(alpha, 0, 0, 0) };
                var bl = new Blend();
                bl.Factors = new float[] { 0f, 0.55f, 1f, 1f };
                bl.Positions = new float[] { 0f, 0.28f, 0.6f, 1f };
                pb.Blend = bl;
                g.FillRectangle(pb, 0, 0, w, h);
            }
        }
    }
    static void Blobs(Graphics g, Random r, int n, float x0, float y0, float x1, float y1, float rmin, float rmax, Color[] cols)
    {
        for (int i = 0; i < n; i++)
        {
            float rr = rmin + (float)r.NextDouble() * (rmax - rmin);
            Ell(g, cols[r.Next(cols.Length)], x0 + (float)r.NextDouble() * (x1 - x0), y0 + (float)r.NextDouble() * (y1 - y0), rr, rr * 0.8f);
        }
    }
    static void Star5(Graphics g, Color c, float cx, float cy, float r)
    {
        var p = new float[20];
        for (int i = 0; i < 10; i++)
        {
            double a = -Math.PI / 2 + i * Math.PI / 5;
            float rr = (i % 2 == 0) ? r : r * 0.42f;
            p[i * 2] = cx + (float)(Math.Cos(a) * rr); p[i * 2 + 1] = cy + (float)(Math.Sin(a) * rr);
        }
        Poly(g, c, p);
    }
    static void MulAlphaRows(Bitmap b, int y0, int y1)
    {
        var rect = new Rectangle(0, 0, b.Width, b.Height);
        var d = b.LockBits(rect, ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
        int bytes = d.Stride * b.Height; byte[] buf = new byte[bytes];
        Marshal.Copy(d.Scan0, buf, 0, bytes);
        for (int y = y0; y < b.Height; y++)
        {
            float t = y >= y1 ? 0f : 1f - (float)(y - y0) / (y1 - y0);
            t = t * t;
            for (int x = 0; x < b.Width; x++) { int i = y * d.Stride + x * 4 + 3; buf[i] = (byte)(buf[i] * t); }
        }
        Marshal.Copy(buf, 0, d.Scan0, bytes); b.UnlockBits(d);
    }

    // ================================================================ BACKGROUNDS
    static Bitmap BgCong(bool title)
    {
        var b = NB(W, H); var g = G(b); var r = new Random(11);
        VGrad(g, 0, 0, W, 760, C("#04071a"), C("#1d2647"));
        Stars(g, 200, W, 520, 1);
        Glow(g, 1560, 170, 320, 320, C("#cdd6ff", 60));
        Ell(g, C("#f1ead0"), 1560, 170, 62, 62);
        Ell(g, C("#d8ceb0", 140), 1538, 156, 14, 11); Ell(g, C("#d8ceb0", 110), 1582, 192, 10, 8); Ell(g, C("#d8ceb0", 90), 1572, 145, 6, 5);
        for (int i = 0; i < 9; i++) Glow(g, r.Next(W), 120 + r.Next(260), 260 + r.Next(200), 40 + r.Next(30), C("#3a4568", 70));
        // hàng cây xa
        Blobs(g, r, 70, -50, 360, W + 50, 520, 50, 120, new Color[] { C("#0a130f"), C("#0c1712"), C("#08100c") });
        // dãy nhà trường
        Rect(g, C("#161b2b"), 260, 300, 1400, 460);
        Poly(g, C("#0e111c"), 230, 300, 1690, 300, 1640, 245, 280, 245);
        for (int fl = 0; fl < 2; fl++)
            for (int i = 0; i < 11; i++)
            {
                float x = 320 + i * 125, y = 350 + fl * 180;
                bool lit = (fl == 0 && i == 3);
                Rect(g, lit ? C("#3c4c62") : C("#0b0e17"), x, y, 80, 110);
                Rect(g, C("#232a3c"), x + 38, y, 4, 110);
                if (lit)
                {
                    Glow(g, x + 40, y + 55, 90, 90, C("#7a90b0", 60));
                    Ell(g, C("#0d1119"), x + 40, y + 52, 13, 14); FillRR(g, C("#0d1119"), x + 24, y + 64, 32, 46, 8);
                }
            }
        Rect(g, C("#1d2335"), 260, 470, 1400, 14);
        // tường rào gạch
        Rect(g, C("#3a332e"), 0, 660, W, 150);
        for (int y = 660; y < 810; y += 30)
        {
            Rect(g, C("#2a2420"), 0, y, W, 3);
            int off = ((y / 30) % 2) * 45;
            for (int x = off; x < W; x += 90) Rect(g, C("#2a2420"), x, y, 3, 30);
        }
        Rect(g, C("#5a524b"), 0, 646, W, 16);
        for (int i = 0; i < 40; i++) Glow(g, r.Next(W), 700 + r.Next(100), 40 + r.Next(50), 20, C("#1a3a1a", 80)); // rêu
        // cổng
        Rect(g, C("#0d1018"), 770, 470, 380, 410);
        Glow(g, 960, 700, 200, 160, C("#2a3550", 90));
        for (float x = 785; x < 1150; x += 28)
        {
            Rect(g, C("#2c2d33"), x, 470, 8, 410); Rect(g, C("#4a4c55"), x, 470, 2, 410);
            Poly(g, C("#3a3b42"), x - 4, 472, x + 12, 472, x + 4, 450);
        }
        foreach (float y in new float[] { 490, 680, 860 }) { Rect(g, C("#2c2d33"), 770, y, 380, 10); Rect(g, C("#4a4c55"), 770, y, 380, 2); }
        Rect(g, C("#15161a"), 957, 470, 6, 410);
        for (int i = 0; i < 60; i++) Ell(g, C("#7a4026", 120), 780 + r.Next(360), 480 + r.Next(390), 2 + r.Next(4), 2 + r.Next(5));
        Ln(g, C("#6a6a70"), 5, 950, 690, 970, 700); Ln(g, C("#6a6a70"), 5, 970, 690, 950, 712); // xích khóa
        Ell(g, C("#5a5a60"), 960, 720, 12, 16);
        foreach (float px in new float[] { 700, 1150 })
        {
            FillRRO(g, C("#4d463f"), C("#2a2420"), 3, px, 420, 70, 460, 4);
            Rect(g, C("#615950"), px - 8, 410, 86, 18);
            Ell(g, C("#615950"), px + 35, 404, 22, 14);
        }
        FillRRO(g, C("#1b3566"), C("#d9c58a"), 4, 640, 345, 640, 82, 8);
        Txt(g, "TRƯỜNG TIỂU HỌC VĨNH NINH", "Segoe UI", 40, FontStyle.Bold, C("#f2ead0"), 960, 362, true);
        // chòi bảo vệ
        Rect(g, C("#4a4434"), 1380, 560, 300, 300);
        Poly(g, C("#2b2620"), 1350, 562, 1710, 562, 1662, 505, 1398, 505);
        Rect(g, C("#d29a3c", 235), 1440, 630, 120, 90);
        Glow(g, 1500, 675, 260, 190, C("#ffb850", 80));
        Rect(g, C("#3a2c18"), 1498, 630, 4, 90); Rect(g, C("#3a2c18"), 1440, 674, 120, 4);
        Rect(g, C("#1e3a1c"), 1525, 690, 14, 30); Rect(g, C("#1e3a1c"), 1529, 680, 6, 12);
        Rect(g, C("#2e2a22"), 1590, 640, 70, 220);
        FillRR(g, C("#d9d2b8"), 1430, 585, 150, 32, 4);
        Txt(g, "BẢO VỆ", "Segoe UI", 22, FontStyle.Bold, C("#5a1a10"), 1505, 587, true);
        // mặt đường
        VGrad(g, 0, 810, W, 270, C("#1b1b20"), C("#09090b"));
        Ell(g, C("#2a3350", 130), 600, 960, 190, 22); Ell(g, C("#2a3350", 110), 1300, 1010, 250, 28);
        Ell(g, C("#e8e0c8", 90), 1300, 1006, 18, 4);
        Ln(g, C("#2a2a30"), 4, 0, 870, W, 860);
        // cột đèn
        Rect(g, C("#1d1f24"), 236, 250, 14, 620);
        Ln(g, C("#1d1f24"), 10, 243, 262, 300, 250);
        Poly(g, C("#2a2c31"), 278, 244, 332, 244, 322, 268, 288, 268);
        Glow(g, 305, 290, 340, 340, C("#ffd27a", 100));
        Ell(g, C("#fff2c0"), 305, 270, 16, 8);
        Glow(g, 300, 890, 320, 60, C("#ffd27a", 70));
        for (int i = 0; i < 16; i++) Glow(g, r.Next(W), 820 + r.Next(90), 320, 60, C("#8a96b0", 34));
        if (title)
        {
            Glow(g, 960, 690, 140, 260, C("#dfe9ee", 40)); // bóng trắng sau cổng
        }
        Grain(g, W, H, 45000, 22, 3); Vignette(g, W, H, 200);
        g.Dispose(); return b;
    }

    static Bitmap BgLop()
    {
        var b = NB(W, H); var g = G(b); var r = new Random(21);
        VGrad(g, 0, 0, W, 720, C("#8f8a63"), C("#78734f"));
        Rect(g, C("#5f5b45"), 0, 0, W, 70);
        Rect(g, C("#4f6650"), 0, 580, W, 140); Rect(g, C("#3c4f3d"), 0, 576, W, 8);
        VGrad(g, 0, 720, W, 360, C("#6e624f"), C("#3a3228"));
        for (int i = -14; i <= 14; i++) Ln(g, C("#000000", 45), 2, 960 + i * 70, 720, 960 + i * 300, 1080);
        foreach (float y in new float[] { 760, 815, 885, 975 }) Rect(g, C("#000000", 45), 0, y, W, 2);
        // đèn tuýp
        foreach (float x in new float[] { 420, 1240 })
        {
            Glow(g, x + 130, 100, 460, 200, C("#fffbe0", 70));
            FillRR(g, C("#f6f8ec"), x, 82, 260, 14, 6);
        }
        // quạt trần
        Rect(g, C("#2e2e2c"), 957, 0, 6, 42);
        Ell(g, C("#4a4a48"), 852, 58, 110, 12); Ell(g, C("#4a4a48"), 1068, 58, 110, 12);
        Ell(g, C("#3a3a3a"), 960, 52, 24, 15);
        // khẩu hiệu
        FillRR(g, C("#b3241f"), 300, 98, 580, 54, 6);
        Txt(g, "TIÊN HỌC LỄ — HẬU HỌC VĂN", "Segoe UI", 32, FontStyle.Bold, C("#ffd84a"), 590, 105, true);
        // bảng đen
        FillRRO(g, C("#5a3d24"), C("#2a1a10"), 3, 170, 165, 840, 365, 10);
        Rect(g, C("#1e3a2c"), 188, 183, 804, 329);
        for (int i = 0; i < 25; i++) Glow(g, 200 + r.Next(780), 200 + r.Next(300), 60 + r.Next(80), 20 + r.Next(30), C("#ffffff", 14));
        Color chalk = C("#f2f2ea", 225);
        Txt(g, "Thứ Sáu, ngày 14 tháng 10", "Segoe Print", 46, FontStyle.Regular, chalk, 225, 200, false);
        Txt(g, "Sĩ số: 5      Vắng: 1 — lớp trưởng (ốm)", "Segoe Print", 32, FontStyle.Regular, chalk, 228, 285, false);
        Txt(g, "trốn tìm!!", "Segoe Print", 30, FontStyle.Regular, C("#f6e7a0", 200), 230, 420, false);
        for (int k = 0; k < 4; k++)
        {
            float x = 690 + k * 70, y = 420;
            using (var p = RP(C("#f2f2ea", 200), 4))
            {
                g.DrawEllipse(p, x - 12, y - 12, 24, 24);
                g.DrawLine(p, x, y + 12, x, y + 50);
                g.DrawLine(p, x, y + 50, x - 14, y + 78); g.DrawLine(p, x, y + 50, x + 14, y + 78);
                g.DrawLine(p, x - 35, y + 28, x + 35, y + 28);
            }
        }
        Rect(g, C("#4a3220"), 180, 524, 820, 14);
        Rect(g, C("#f4f4f0"), 300, 518, 28, 7); Rect(g, C("#f0c0c0"), 360, 518, 20, 7);
        // cửa sổ
        foreach (float wx in new float[] { 1110, 1380 })
        {
            FillRR(g, C("#5d4a33"), wx - 10, 170, 250, 340, 6);
            VGrad(g, wx, 180, 230, 320, C("#0a1530"), C("#16264a"));
            g.SetClip(new RectangleF(wx, 180, 230, 320));
            Ell(g, C("#e8e0c0", 160), wx + 180, 220, 10, 10);
            Blobs(g, r, 12, wx - 40, 300, wx + 280, 420, 40, 80, new Color[] { C("#050a09"), C("#071010") });
            Rect(g, C("#050807"), wx + 60, 380, 30, 120);
            g.ResetClip();
            for (int k = 1; k <= 4; k++) Rect(g, C("#2d2418"), wx + 46 * k - 3, 180, 6, 320);
            Rect(g, C("#5d4a33"), wx, 338, 230, 8);
            Rect(g, C("#7a6448"), wx - 16, 506, 262, 12);
        }
        // cửa lớp
        FillRRO(g, C("#6b4a2c"), C("#2a1a10"), 3, 1660, 220, 230, 560, 6);
        StrokeRR(g, C("#4a3018"), 4, 1690, 250, 170, 220, 4); StrokeRR(g, C("#4a3018"), 4, 1690, 500, 170, 250, 4);
        FillRR(g, C("#e8e0c0"), 1700, 168, 150, 42, 6);
        Txt(g, "LỚP 5A", "Segoe UI", 28, FontStyle.Bold, C("#5a1a10"), 1775, 172, true);
        Ell(g, C("#c7a65a"), 1690, 520, 9, 18);
        // khe âm dương
        EllO(g, C("#1a1a1a"), C("#c7a65a"), 4, 1700, 460, 22, 22);
        using (var br = new SolidBrush(C("#e8e4d8"))) g.FillPie(br, 1680, 440, 40, 40, 270, 180);
        // bục + bàn cô
        Rect(g, C("#5a4632"), 540, 760, 760, 40); Rect(g, C("#3e3022"), 540, 796, 760, 10);
        Rect(g, C("#4e3520"), 835, 530, 100, 80); Rect(g, C("#3a2616"), 845, 540, 80, 8);
        FillRRO(g, C("#7b5434"), C("#2a1a10"), 3, 630, 596, 490, 32, 4);
        Rect(g, C("#5c3d24"), 650, 628, 450, 140);
        HGrad(g, 650, 628, 450, 140, C("#000000", 0), C("#000000", 60));
        FillRRO(g, C("#6b4a2e"), C("#2a1a10"), 2, 760, 648, 230, 62, 4);
        FillRR(g, C("#202020"), 850, 662, 52, 36, 4);
        for (int k = 0; k < 3; k++) Ell(g, C("#60ff90", 200), 862 + k * 14, 680, 3, 3);
        Poly(g, C("#efe8d8"), 680, 596, 790, 590, 800, 600, 690, 606);
        FillRR(g, C("#3a6aa8"), 1040, 560, 34, 40, 6);
        Ln(g, C("#c03030"), 3, 1050, 560, 1046, 540); Ln(g, C("#303030"), 3, 1060, 560, 1066, 542);
        // bàn học sinh
        Poly(g, C("#7a5436"), 120, 740, 520, 740, 548, 782, 92, 782);
        Rect(g, C("#5a3d26"), 92, 782, 456, 70);
        Rect(g, C("#3e2a18"), 110, 852, 14, 60); Rect(g, C("#3e2a18"), 515, 852, 14, 60);
        Poly(g, C("#80593a"), 30, 858, 610, 858, 650, 922, 0, 922);
        Rect(g, C("#5a3d26"), 0, 922, 650, 158);
        HGrad(g, 0, 922, 650, 158, C("#000000", 0), C("#000000", 70));
        Txt(g, "5A mãi mãi là bạn", "Segoe Print", 26, FontStyle.Regular, C("#3a2414", 210), 170, 868, false);
        FillRRO(g, C("#3c6aa8"), C("#1a2a44"), 3, 440, 790, 96, 76, 22);
        Rect(g, C("#2c4a7a"), 456, 812, 64, 6);
        Poly(g, C("#7a5436"), 1300, 878, 1920, 878, 1920, 940, 1262, 940);
        Rect(g, C("#5a3d26"), 1262, 940, 658, 140);
        Grain(g, W, H, 50000, 18, 4); Vignette(g, W, H, 170);
        g.Dispose(); return b;
    }

    static Bitmap BgSan(bool night)
    {
        var b = NB(W, H); var g = G(b); var r = new Random(31);
        if (night) { VGrad(g, 0, 0, W, 620, C("#040916"), C("#16213c")); Stars(g, 160, W, 300, 2); Ell(g, C("#e8e2c8"), 1300, 100, 30, 30); Glow(g, 1300, 100, 160, 160, C("#c8d0ff", 50)); }
        else { VGrad(g, 0, 0, W, 620, C("#8fc3ea"), C("#f7e4bc")); Glow(g, 1560, 110, 420, 300, C("#fff0c0", 160)); for (int i = 0; i < 6; i++) Glow(g, r.Next(W), 60 + r.Next(120), 220, 40, C("#ffffff", 120)); }
        // dãy lớp học 2 tầng
        Color wall = N(night, "#252c3a", "#e8cc86"), trim = N(night, "#1a1f2b", "#c8a060"), roof = N(night, "#2a1a18", "#8a3a26");
        Rect(g, wall, 0, 200, W, 400);
        Poly(g, roof, 0, 205, W, 205, W, 165, 0, 165);
        Rect(g, trim, 0, 360, W, 44);
        for (float x = 0; x < W; x += 160)
        {
            Rect(g, trim, x, 200, 24, 400);
            Rect(g, N(night, "#101521", "#5d7287"), x + 55, 235, 70, 95);
            Rect(g, trim, x + 88, 235, 4, 95);
        }
        for (float x = 30; x < W; x += 20) Rect(g, N(night, "#3a4152", "#f0e0b0"), x, 370, 5, 30);
        Rect(g, N(night, "#3a4152", "#f6ead0"), 0, 366, W, 6);
        // tầng trệt: cửa sổ + cửa
        for (float x = 0; x < W; x += 160)
            if (!(x == 320 || x == 640 || x == 1280)) Rect(g, N(night, "#0e131d", "#5d7287"), x + 55, 450, 70, 90);
        Rect(g, N(night, "#353c4a", "#d9caa8"), 0, 590, W, 20);
        string[] names = { "TÀI VỤ", "WC", "5A" };
        float[] dx = { 330, 640, 1300 }; float[] dw = { 100, 80, 100 };
        for (int i = 0; i < 3; i++)
        {
            FillRRO(g, N(night, "#3a2c20", "#7a5a3a"), C("#1a1008"), 3, dx[i], 450, dw[i], 145, 3);
            Ell(g, C("#c7a65a"), dx[i] + dw[i] - 14, 525, 5, 5);
            FillRR(g, N(night, "#9a9480", "#f2ecd8"), dx[i] - 6, 418, dw[i] + 12, 28, 4);
            Txt(g, names[i], "Segoe UI", 19, FontStyle.Bold, C("#5a1a10"), dx[i] + dw[i] / 2, 419, true);
        }
        if (night)
        {
            foreach (float lx in new float[] { 380, 1350, 900 })
            { Glow(g, lx, 430, 160, 120, C("#ffd890", 80)); Ell(g, C("#fff2c0"), lx, 404, 8, 6); }
        }
        // bậc thềm trước 5A
        Rect(g, N(night, "#3e434e", "#d8d2c0"), 1250, 600, 200, 18);
        Rect(g, N(night, "#353a44", "#c8c0aa"), 1262, 618, 176, 16);
        Rect(g, N(night, "#2c3038", "#b8b098"), 1274, 634, 152, 16);
        // sân
        VGrad(g, 0, 610, W, 470, N(night, "#22252c", "#cbb791"), N(night, "#0c0d10", "#9a845e"));
        for (int i = 0; i < 9; i++) Rect(g, C("#000000", 30), 0, 650 + i * i * 6, W, 2);
        // dây điện cũ trên sân
        Bez(g, C("#111111", 230), 7, 960, 905, 1060, 950, 1180, 900, 1320, 965);
        // cây bàng
        Color bark = N(night, "#20160f", "#5a3e26");
        Poly(g, bark, 140, 905, 330, 905, 280, 640, 262, 420, 214, 420, 196, 640);
        Ln(g, bark, 34, 240, 470, 90, 330); Ln(g, bark, 28, 245, 460, 420, 320); Ln(g, bark, 22, 240, 440, 250, 260);
        Color[] crown = night ? new Color[] { C("#0b1a12"), C("#0f2218"), C("#08140e") } : new Color[] { C("#3f7a3a"), C("#2e6230"), C("#5a9a48"), C("#4a8a40") };
        Blobs(g, r, 55, -160, -60, 560, 250, 70, 140, crown);
        if (!night) Blobs(g, r, 18, -60, 20, 520, 300, 12, 22, new Color[] { C("#c8582a"), C("#e08a30") });
        else Blobs(g, r, 25, -60, 0, 520, 280, 30, 60, new Color[] { C("#16301f", 180) });
        FillRR(g, C("#0e0905"), 186, 728, 86, 98, 30);
        Rect(g, N(night, "#4a3826", "#9a7a52"), 180, 745, 100, 70);
        Ell(g, C("#202020"), 190, 755, 3, 3); Ell(g, C("#202020"), 270, 755, 3, 3); Ell(g, C("#202020"), 190, 805, 3, 3); Ell(g, C("#202020"), 270, 805, 3, 3);
        Txt(g, "3C", "Segoe Print", 32, FontStyle.Bold, C("#1e140a", 200), 208, 748, false);
        // phòng bảo vệ
        Rect(g, N(night, "#3e3a30", "#d8c9a0"), 420, 610, 340, 280);
        Poly(g, N(night, "#1e1a16", "#7a4a30"), 398, 612, 782, 612, 760, 568, 420, 568);
        Rect(g, N(night, "#241a10", "#6a4a2c"), 460, 690, 100, 200);
        if (night) { Rect(g, C("#d29a3c", 235), 600, 680, 130, 90); Glow(g, 665, 725, 250, 170, C("#ffb850", 85)); }
        else Rect(g, C("#4a5a6a"), 600, 680, 130, 90);
        Rect(g, C("#2a1c10"), 600, 676, 130, 6); Rect(g, C("#2a1c10"), 600, 768, 130, 6);
        Rect(g, N(night, "#3e2e1c", "#8a6a44"), 600, 680, 60, 90); Rect(g, C("#2a1c10"), 657, 680, 5, 90);
        FillRR(g, C("#efe6cc"), 586, 624, 160, 32, 4);
        Txt(g, "PHÒNG BẢO VỆ", "Segoe UI", 20, FontStyle.Bold, C("#5a1a10"), 666, 627, true);
        // cột cờ
        Rect(g, N(night, "#3a3834", "#8a8478"), 830, 760, 140, 40);
        Rect(g, N(night, "#2c2a28", "#76705f"), 845, 742, 110, 20);
        Rect(g, N(night, "#6a6e78", "#c8c8c8"), 896, 92, 8, 660);
        Ell(g, N(night, "#8a8e98", "#e8d070"), 900, 88, 8, 8);
        using (var p = new GraphicsPath())
        {
            p.AddBezier(904, 104, 950, 96, 990, 118, 1032, 110);
            p.AddLine(1032, 110, 1024, 180);
            p.AddBezier(1024, 180, 990, 188, 950, 170, 904, 182);
            p.CloseFigure();
            using (var br = new SolidBrush(N(night, "#6a1212", "#d8261e"))) g.FillPath(br, p);
        }
        Star5(g, N(night, "#9a8420", "#ffd83a"), 966, 144, 20);
        // bể nước
        Poly(g, N(night, "#1a2a3a", "#5a8aa8"), 1075, 642, 1215, 642, 1230, 662, 1060, 662);
        FillRRO(g, N(night, "#4a4c50", "#b0aea4"), C("#1a1a1a"), 3, 1060, 660, 170, 150, 6);
        Rect(g, N(night, "#3a3c40", "#9a988e"), 1060, 660, 170, 12);
        Ln(g, C("#5a5a5a"), 8, 1230, 720, 1258, 720); Ln(g, C("#5a5a5a"), 8, 1258, 720, 1258, 740);
        // bảng quy hoạch
        Rect(g, C("#3a3a3a"), 1462, 690, 10, 112); Rect(g, C("#3a3a3a"), 1588, 690, 10, 112);
        FillRRO(g, N(night, "#6a6a62", "#ece8d6"), C("#2a2a2a"), 3, 1440, 560, 180, 130, 4);
        Rect(g, C("#b3241f"), 1446, 566, 168, 18);
        Txt(g, "QUY HOẠCH", "Segoe UI", 13, FontStyle.Bold, C("#ffffff"), 1530, 566, true);
        for (int k = 1; k < 4; k++) { Rect(g, C("#5a6a5a"), 1450 + k * 40, 588, 2, 96); Rect(g, C("#5a6a5a"), 1450, 588 + k * 24, 160, 2); }
        Rect(g, N(night, "#4a7a4a", "#6aaa5a"), 1532, 638, 36, 20);
        // nhà xe
        Rect(g, C("#2a2a2c"), 1668, 625, 12, 280); Rect(g, C("#2a2a2c"), 1900, 615, 12, 290);
        Poly(g, N(night, "#2a2e34", "#7a8088"), 1640, 625, 1920, 600, 1920, 642, 1640, 655);
        for (float x = 1650; x < 1920; x += 22) Ln(g, C("#000000", 60), 2, x, 628 - (x - 1640) * 0.09f, x, 652 - (x - 1640) * 0.05f);
        for (int k = 0; k < 3; k++)
        {
            float bx = 1700 + k * 75, by = 850 + (k % 2) * 14;
            Color bc = N(night, "#141414", "#3a3a3a");
            using (var p = RP(bc, 5)) { g.DrawEllipse(p, bx - 36, by - 36, 72, 72); g.DrawEllipse(p, bx + 54, by - 36, 72, 72); }
            Ln(g, N(night, "#3a1a14", "#9a3a2a"), 6, bx, by, bx + 40, by - 50); Ln(g, N(night, "#3a1a14", "#9a3a2a"), 6, bx + 40, by - 50, bx + 90, by);
            Ln(g, N(night, "#3a1a14", "#9a3a2a"), 6, bx + 40, by - 50, bx + 80, by - 52); Ln(g, bc, 6, bx + 80, by - 52, bx + 90, by);
            Ln(g, bc, 8, bx + 30, by - 64, bx + 52, by - 64); Ln(g, bc, 5, bx + 78, by - 58, bx + 92, by - 72);
        }
        Ell(g, N(night, "#8a8a8a", "#d8d8d8"), 1867, 784, 6, 6);
        if (night) for (int i = 0; i < 16; i++) Glow(g, r.Next(W), 860 + r.Next(120), 320, 50, C("#8a96b0", 30));
        else { Glow(g, 1700, 300, 900, 500, C("#fff0c8", 60)); }
        Grain(g, W, H, 50000, night ? 22 : 12, 5); Vignette(g, W, H, night ? 210 : 110);
        g.Dispose(); return b;
    }

    static Bitmap BgBaoVeCua()
    {
        var b = NB(W, H); var g = G(b); var r = new Random(41);
        VGrad(g, 0, 0, W, H, C("#2e1d0e"), C("#0c0703"));
        for (float x = 0; x < W; x += 90) Rect(g, C("#000000", 50), x, 0, 3, 640);
        Ln(g, C("#111111"), 3, 960, 0, 960, 100);
        Glow(g, 960, 120, 520, 360, C("#ffb850", 70)); Ell(g, C("#ffe2a0"), 960, 112, 16, 20);
        Rect(g, C("#20140a"), 0, 640, W, 440);
        // giường + bác Thọ ngủ
        Rect(g, C("#4a3420"), 200, 660, 960, 110); Rect(g, C("#2a1c10"), 200, 770, 20, 120); Rect(g, C("#2a1c10"), 1140, 770, 20, 120);
        Ell(g, C("#8a7a60"), 300, 640, 95, 40);
        Ell(g, C("#5c4a36"), 700, 640, 420, 80);
        Ell(g, C("#6a5640"), 680, 620, 360, 50);
        EllO(g, C("#c08e66"), OL, 3, 330, 600, 58, 62);
        Rect(g, C("#9a958c"), 278, 560, 30, 40);
        Arc(g, C("#3a2418"), 4, 318, 600, 22, 10, 0, 180); Arc(g, C("#3a2418"), 4, 345, 600, 22, 10, 0, 180);
        Ell(g, C("#5a1f18"), 340, 636, 10, 7);
        Ln(g, C("#6f6e40"), 38, 520, 680, 470, 820); Ell(g, C("#c08e66"), 466, 830, 22, 22);
        Rect(g, C("#1e3a1c"), 520, 860, 26, 70); Rect(g, C("#1e3a1c"), 527, 840, 12, 24);
        // bàn & chai rượu
        Rect(g, C("#5a3a20"), 1220, 640, 420, 24); Rect(g, C("#3a2410"), 1240, 664, 16, 220); Rect(g, C("#3a2410"), 1610, 664, 16, 220);
        float[] bxs = { 1270, 1330, 1400 }; string[] bcs = { "#2f6b3a", "#6a3a1a", "#2f6b3a" };
        for (int i = 0; i < 3; i++) { FillRR(g, C(bcs[i], 220), bxs[i], 540, 40, 100, 10); Rect(g, C(bcs[i], 220), bxs[i] + 13, 500, 14, 44); }
        FillRR(g, C("#6f6e40"), 1480, 600, 110, 40, 16); Ell(g, C("#d9b440"), 1535, 615, 8, 8);
        // thanh treo chìa khóa
        Rect(g, C("#6a4a2a"), 1350, 280, 320, 24);
        for (int k = 0; k < 4; k++) Ell(g, C("#b0a090"), 1380 + k * 80, 300, 5, 5);
        Glow(g, 1460, 380, 140, 140, C("#ffd070", 50));
        using (var p = RP(C("#c8a24a"), 5)) g.DrawEllipse(p, 1440, 300, 40, 40);
        Rect(g, C("#c8a24a"), 1452, 338, 8, 70); Rect(g, C("#c8a24a"), 1460, 380, 14, 6); Rect(g, C("#c8a24a"), 1460, 395, 10, 6);
        Rect(g, C("#a8a8a8"), 1474, 336, 7, 60);
        FillRRO(g, C("#efe8d8"), C("#7a6a50"), 2, 1430, 410, 80, 40, 4);
        Txt(g, "TÀI VỤ", "Segoe UI", 16, FontStyle.Bold, C("#5a1a10"), 1470, 418, true);
        Ell(g, C("#2a1a0a", 200), 1505, 446, 10, 8);
        using (var p = RP(C("#8a8a8a"), 4)) g.DrawEllipse(p, 1580, 300, 30, 30);
        Rect(g, C("#8a8a8a"), 1592, 328, 6, 50);
        // khung ô cửa lùa (tiền cảnh)
        Rect(g, C("#170d06"), 0, 0, W, 90); Rect(g, C("#170d06"), 0, 950, W, 130);
        Rect(g, C("#170d06"), 0, 0, 170, H); Rect(g, C("#170d06"), 1750, 0, 170, H);
        Rect(g, C("#2a1a0c"), 170, 90, 18, 860); Rect(g, C("#2a1a0c"), 1732, 90, 18, 860);
        Rect(g, C("#2a1a0c"), 170, 90, 1580, 14); Rect(g, C("#2a1a0c"), 170, 936, 1580, 14);
        Rect(g, C("#9ab0c0", 26), 188, 104, 560, 832); Rect(g, C("#3a2410"), 640, 104, 24, 832);
        for (int i = 0; i < 5; i++) Ln(g, C("#ffffff", 22), 6, 240 + i * 90, 120, 200 + i * 90, 300);
        Grain(g, W, H, 45000, 24, 6); Vignette(g, W, H, 220);
        g.Dispose(); return b;
    }

    static Bitmap BgTaiVu()
    {
        var b = NB(W, H); var g = G(b); var r = new Random(51);
        VGrad(g, 0, 0, W, 760, C("#5f5a50"), C("#48443c"));
        VGrad(g, 0, 760, W, 320, C("#3a342c"), C("#171310"));
        for (int i = 0; i < 12; i++) Rect(g, C("#000000", 40), 0, 790 + i * i * 2.4f, W, 2);
        for (int i = 0; i < 26; i++) Glow(g, r.Next(W), r.Next(260), 160 + r.Next(220), 80 + r.Next(120), C("#0a0806", 90 + r.Next(60)));
        Rect(g, C("#000000", 60), 0, 740, W, 20);
        // cửa sổ song sắt
        FillRR(g, C("#3a3028"), 1040, 110, 270, 200, 4);
        VGrad(g, 1052, 122, 246, 176, C("#0e1a30"), C("#1c2c4a"));
        for (int k = 1; k < 6; k++) Rect(g, C("#1a1a1a"), 1052 + k * 41, 122, 6, 176);
        Glow(g, 1175, 330, 260, 120, C("#6a80b0", 30));
        // lịch
        Ell(g, C("#2a2a2a"), 255, 160, 5, 5);
        Rect(g, C("#efe8d8"), 180, 170, 150, 210);
        Rect(g, C("#b3241f"), 180, 170, 150, 44);
        Txt(g, "THÁNG 10", "Segoe UI", 22, FontStyle.Bold, C("#ffffff"), 255, 178, true);
        Txt(g, "14", "Segoe UI Black", 96, FontStyle.Regular, C("#b3241f"), 255, 205, true);
        Txt(g, "THỨ SÁU", "Segoe UI", 20, FontStyle.Bold, C("#3a2a1a"), 255, 330, true);
        Glow(g, 325, 378, 70, 60, C("#140a04", 230)); Glow(g, 182, 175, 30, 30, C("#140a04", 160));
        // bàn làm việc
        Rect(g, C("#5a3c24"), 290, 600, 340, 24); Rect(g, C("#4a3020"), 300, 624, 320, 150);
        Rect(g, C("#2a1a10"), 460, 630, 4, 140); Rect(g, C("#2a1a10"), 300, 690, 320, 3);
        for (int k = 0; k < 4; k++) Poly(g, C("#e8e0c8", 220 - k * 20), 320 + k * 6, 590 - k * 6, 440 + k * 6, 586 - k * 6, 446 + k * 6, 600 - k * 6, 326 + k * 6, 602 - k * 6);
        FillRR(g, C("#2a4a7a"), 500, 556, 90, 44, 4); FillRR(g, C("#7a2a2a"), 506, 530, 80, 28, 4);
        // tủ tài liệu
        FillRRO(g, C("#6d7270"), C("#1a1a1a"), 3, 700, 260, 260, 540, 6);
        HGrad(g, 700, 260, 260, 540, C("#ffffff", 30), C("#000000", 60));
        for (int k = 0; k < 4; k++)
        {
            float y = 280 + k * 128;
            FillRRO(g, C("#7d8280"), C("#3a3c3e"), 2, 720, y, 220, 112, 4);
            Rect(g, C("#2c2e30"), 800, y + 46, 60, 10);
            Rect(g, C("#e8e4d8"), 805, y + 18, 50, 18);
        }
        FillRR(g, C("#1e1e1e"), 878, 700, 48, 30, 4);
        for (int k = 0; k < 3; k++) Ell(g, C("#ff7050", 200), 890 + k * 12, 715, 3, 3);
        // bảng điện
        Glow(g, 1100, 360, 140, 110, C("#000000", 160));
        FillRRO(g, C("#8a8e8a"), C("#2a2a2a"), 3, 1020, 380, 160, 200, 4);
        Rect(g, C("#6a6e6a"), 1098, 384, 3, 192);
        Poly(g, C("#ffd030"), 1100, 410, 1135, 470, 1065, 470);
        Poly(g, C("#1a1a1a"), 1104, 422, 1090, 448, 1102, 448, 1094, 466, 1114, 440, 1102, 440, 1110, 422);
        Ell(g, C("#2a2a2a"), 1160, 480, 6, 8);
        Bez(g, C("#141414"), 11, 1060, 578, 1050, 700, 980, 830, 700, 905);
        Bez(g, C("#1c1c1c"), 9, 1140, 578, 1160, 680, 1220, 760, 1200, 860);
        Glow(g, 760, 900, 160, 40, C("#000000", 120));
        // cửa ra vào
        FillRRO(g, C("#5a3c22"), C("#1a1008"), 3, 1440, 200, 240, 620, 4);
        VGrad(g, 1440, 200, 240, 620, C("#000000", 140), C("#000000", 20));
        StrokeRR(g, C("#3a2410"), 4, 1470, 240, 180, 230, 4);
        Ell(g, C("#b09040"), 1462, 540, 8, 14);
        for (int i = 0; i < 70; i++)
        {
            float x = 1470 + r.Next(180), y = 520 + r.Next(130);
            Ln(g, C("#d8c0a0", 120 + r.Next(80)), 2, x, y, x + r.Next(9) - 4, y + 10 + r.Next(26));
        }
        Grain(g, W, H, 50000, 22, 7); Vignette(g, W, H, 200);
        g.Dispose(); return b;
    }

    static void Hand(Graphics g, Color c, float x, float y, float s)
    {
        Ell(g, c, x, y, 16 * s, 19 * s);
        for (int k = 0; k < 4; k++) Ln(g, c, 7 * s, x - 11 * s + k * 7.5f * s, y - 12 * s, x - 16 * s + k * 10 * s, y - 38 * s);
        Ln(g, c, 7 * s, x + 14 * s, y, x + 30 * s, y - 14 * s);
    }

    static Bitmap BgBiMat(bool altar)
    {
        var b = NB(W, H); var g = G(b); var r = new Random(61);
        VGrad(g, 0, 0, W, H, C("#2b2219"), C("#0e0a07"));
        VGrad(g, 360, 120, 1200, 640, C("#3a2e24"), C("#241b14"));
        Poly(g, C("#1c1510"), 0, 0, 360, 120, 360, 760, 0, 1080);
        Poly(g, C("#1c1510"), W, 0, 1560, 120, 1560, 760, W, 1080);
        Poly(g, C("#120d0a"), 0, 0, W, 0, 1560, 120, 360, 120);
        Poly(g, C("#1e1812"), 360, 760, 1560, 760, W, H, 0, H);
        for (int i = 0; i < 30; i++) Glow(g, 360 + r.Next(1200), 120 + r.Next(250), 140 + r.Next(160), 60 + r.Next(80), C("#050302", 120));
        for (int i = 0; i < 8; i++)
        {
            float x = 400 + r.Next(1100), y = 150 + r.Next(400);
            Ln(g, C("#0a0604", 200), 2, x, y, x + r.Next(60) - 30, y + 40 + r.Next(60));
        }
        foreach (var hp in new float[][] { new float[] { 700, 430, 1 }, new float[] { 770, 470, 0.9f }, new float[] { 1240, 400, 1.1f }, new float[] { 560, 540, 0.8f } })
            Hand(g, C("#0e0806", 190), hp[0], hp[1], hp[2]);
        Poly(g, C("#140e0a"), 420, 880, 520, 760, 560, 770, 470, 900);
        Rect(g, C("#140e0a"), 470, 760, 120, 16);
        Blobs(g, r, 300, 200, 820, 1720, 1060, 3, 9, new Color[] { C("#2a2420", 160), C("#3a332c", 140), C("#0a0806", 160) });
        Ell(g, C("#2a2420"), 1400, 830, 150, 42);
        Glow(g, 1400, 815, 160, 55, C("#ff6a20", altar ? 40 : 70));
        for (int i = 0; i < 14; i++) Ell(g, C("#ff8a3a", 220), 1300 + r.Next(200), 810 + r.Next(30), 2.5f, 2.5f);
        if (!altar)
        {
            using (var br = new LinearGradientBrush(new RectangleF(1050, 120, 500, 720), C("#fff4d0", 70), C("#fff4d0", 5), 90f))
                g.FillPolygon(br, Pts(new float[] { 1060, 120, 1140, 120, 1520, 830, 1280, 830 }));
            Glow(g, 1400, 805, 26, 18, C("#ffe8a0", 200));
            Ell(g, C("#fffbe8"), 1400, 805, 4, 4);
        }
        else
        {
            Glow(g, 960, 640, 950, 520, C("#ff9a40", 60));
            Rect(g, C("#5a2416"), 760, 494, 400, 66);
            Rect(g, C("#6a2a1a"), 640, 556, 640, 28);
            Rect(g, C("#9a1c16"), 660, 584, 600, 176);
            Rect(g, C("#d8a83a"), 660, 600, 600, 4); Rect(g, C("#d8a83a"), 660, 740, 600, 4);
            for (float x = 664; x < 1260; x += 14) Ln(g, C("#d8a83a", 200), 3, x, 760, x, 776);
            Txt(g, "卍", "Segoe UI Symbol", 60, FontStyle.Bold, C("#d8a83a", 160), 960, 630, true);
            foreach (float cxp in new float[] { 590, 1330 })
            {
                Rect(g, C("#e8dcc0"), cxp, 640, 20, 92); Rect(g, C("#c8b890"), cxp + 14, 640, 6, 92);
                Glow(g, cxp + 10, 620, 110, 130, C("#ffb040", 90));
                Ell(g, C("#ffd36a"), cxp + 10, 626, 7, 14); Ell(g, C("#fff6d0"), cxp + 10, 630, 3, 6);
            }
            string[] pc = { "#f2b8c8", "#b8d0f2", "#f2e2a0", "#b8e8c0", "#eeeeee" };
            for (int k = 0; k < 5; k++)
            {
                float x = 380 + k * 58, y = 760 - k * 6;
                Poly(g, C(pc[k]), x, y - 60, x + 26, y + 30, x - 26, y + 30);
                Ell(g, C(pc[k]), x, y - 70, 15, 15);
                Ell(g, C("#2a1a1a"), x - 5, y - 72, 2, 2); Ell(g, C("#2a1a1a"), x + 5, y - 72, 2, 2);
                Ell(g, C("#d83a3a"), x - 12, y - 10, 3, 3); Ell(g, C("#3aa860"), x - 7, y - 8, 3, 3);
            }
            Ell(g, C("#c8c0b0"), 1460, 860, 70, 16);
            Ell(g, C("#f08a20"), 1440, 846, 16, 16); Ell(g, C("#f09a30"), 1474, 848, 15, 15); Ell(g, C("#e07a18"), 1458, 834, 15, 15);
        }
        Grain(g, W, H, 55000, 22, 8); Vignette(g, W, H, 220);
        g.Dispose(); return b;
    }

    static Bitmap BgUMinh()
    {
        var b = NB(W, H); var g = G(b); var r = new Random(71);
        VGrad(g, 0, 0, W, H, C("#020309"), C("#0a0e19"));
        for (int i = 0; i < 10; i++) Glow(g, r.Next(W), 200 + r.Next(500), 500, 80, C("#3a4a6a", 40));
        using (var br = new LinearGradientBrush(new RectangleF(700, 0, 520, 760), C("#c8d8ff", 50), C("#c8d8ff", 0), 90f))
            g.FillPolygon(br, Pts(new float[] { 880, 0, 1040, 0, 1240, 760, 680, 760 }));
        Ell(g, C("#0e1218"), 960, 1010, 1400, 260);
        Glow(g, 960, 790, 520, 130, C("#000000", 150));
        Ell(g, C("#2a241e"), 960, 770, 340, 115);
        Glow(g, 960, 735, 300, 80, C("#4e4232", 180));
        for (int i = 0; i < 60; i++)
        {
            double a = r.NextDouble() * Math.PI * 2; float rr = (float)r.NextDouble();
            float x = 960 + (float)Math.Cos(a) * 320 * rr, y = 770 + (float)Math.Sin(a) * 100 * rr;
            Ln(g, C("#1a2418", 200), 2, x, y, x + r.Next(7) - 3, y - 8 - r.Next(10));
        }
        PolyO(g, C("#4a3626"), C("#1a1008"), 3, 912, 490, 1008, 490, 1014, 720, 906, 720);
        Ell(g, C("#4a3626"), 960, 492, 48, 22);
        for (int k = 0; k < 5; k++) Rect(g, C("#c8b090", 60), 930, 530 + k * 30, 60, 3);
        for (int k = 0; k < 3; k++)
        {
            float x = 930 + k * 30;
            Ln(g, C("#6a3a1a"), 3, x, 745, x + (k - 1) * 4, 700);
            Ell(g, C("#ff4a1a"), x + (k - 1) * 4, 700, 3, 3);
            Bez(g, C("#c8c8d8", 50), 3, x + (k - 1) * 4, 698, x + 20, 640, x - 20, 600, x + 10, 540);
        }
        for (int i = 0; i < 12; i++) Glow(g, r.Next(W), 300 + r.Next(600), 30, 30, C("#a8e0ff", 90));
        for (int i = 0; i < 12; i++) Glow(g, r.Next(W), 880 + r.Next(150), 420, 60, C("#a0aac0", 36));
        Grain(g, W, H, 40000, 20, 9); Vignette(g, W, H, 230);
        g.Dispose(); return b;
    }

    static Bitmap Flowers()
    {
        var b = NB(W, H); var g = G(b); var r = new Random(81);
        for (int i = 0; i < 110; i++)
        {
            double a = r.NextDouble() * Math.PI * 2; float rr = 0.55f + (float)r.NextDouble() * 0.6f;
            float x = 960 + (float)Math.Cos(a) * 420 * rr, y = 775 + (float)Math.Sin(a) * 150 * rr;
            float s = 7 + (float)r.NextDouble() * 6;
            Glow(g, x, y, s * 4, s * 3, C("#ffffff", 40));
            Ln(g, C("#4a7a4a"), 2, x, y, x, y + s * 2.2f);
            for (int k = 0; k < 5; k++)
            {
                double pa = k * Math.PI * 2 / 5 + a;
                Ell(g, C("#fbfbf4"), x + (float)Math.Cos(pa) * s * 0.9f, y + (float)Math.Sin(pa) * s * 0.7f, s * 0.75f, s * 0.6f);
            }
            Ell(g, C("#ffd84a"), x, y, s * 0.35f, s * 0.35f);
        }
        g.Dispose(); return b;
    }

    static Bitmap Flames(int seed)
    {
        var b = NB(W, 620); var g = G(b); var r = new Random(seed);
        for (int i = 0; i < 70; i++)
        {
            float x = (float)r.NextDouble() * W, h = 140 + (float)r.NextDouble() * 420, w = 60 + (float)r.NextDouble() * 110;
            float sway = (float)(r.NextDouble() - 0.5) * 80;
            FlameShape(g, x, 620, w, h, sway, C("#ff3a00", 190), C("#ff9a20", 0));
            FlameShape(g, x + sway * 0.1f, 620, w * 0.5f, h * 0.6f, sway * 0.5f, C("#ffe08a", 210), C("#ffb040", 0));
        }
        for (int i = 0; i < 60; i++) Ell(g, C("#ffd070", 200), (float)r.NextDouble() * W, (float)r.NextDouble() * 400, 2, 2);
        g.Dispose(); return b;
    }
    static void FlameShape(Graphics g, float x, float by, float w, float h, float sway, Color bot, Color top)
    {
        using (var p = new GraphicsPath())
        {
            p.AddBezier(x - w / 2, by, x - w / 2, by - h * 0.45f, x + sway - w * 0.1f, by - h * 0.7f, x + sway, by - h);
            p.AddBezier(x + sway, by - h, x + sway + w * 0.15f, by - h * 0.6f, x + w / 2, by - h * 0.4f, x + w / 2, by);
            p.CloseFigure();
            using (var br = new LinearGradientBrush(new RectangleF(x - w, by - h - 1, w * 2, h + 2), top, bot, 90f)) g.FillPath(br, p);
        }
    }

    // ================================================================ CHARACTERS
    class Kid
    {
        public string id, hair; public bool girl, glasses, chubby, monitor, ghost;
        public Color hairC, acc;
    }
    const float KCX = 260, EY = 262, EX1 = KCX - 55, EX2 = KCX + 55;

    static void Arm(Graphics g, float sx, float sy, float ex, float ey, float hx, float hy, Color sleeve, Color skin, bool bracelet)
    {
        float mx = sx + (ex - sx) * 0.6f, my = sy + (ey - sy) * 0.6f;
        Ln(g, OL, 58, sx, sy, mx, my); Ln(g, OL, 38, mx, my, ex, ey); Ln(g, OL, 38, ex, ey, hx, hy);
        Ln(g, skin, 30, mx, my, ex, ey); Ln(g, skin, 30, ex, ey, hx, hy);
        Ln(g, sleeve, 50, sx, sy, mx, my);
        EllO(g, skin, OL, 3.5f, hx, hy, 20, 20);
        if (bracelet)
        {
            float bx = ex + (hx - ex) * 0.78f, by = ey + (hy - ey) * 0.78f;
            float dx = hx - ex, dy = hy - ey; float len = (float)Math.Sqrt(dx * dx + dy * dy); float px = -dy / len, py = dx / len;
            for (int k = -2; k <= 2; k++)
            {
                Color bc = (k % 2 == 0) ? C("#d83a3a") : C("#3aa860");
                EllO(g, bc, C("#1a1010", 200), 1.5f, bx + px * k * 8.5f, by + py * k * 8.5f, 5.5f, 5.5f);
            }
        }
    }

    static void HairCap(Graphics g, Kid k, float bangY, float hw)
    {
        g.SetClip(new RectangleF(0, 0, 520, bangY));
        Ell(g, k.hairC, KCX, 240, hw / 2 + 14, 160);
        g.ResetClip();
    }

    static Bitmap DrawKid(Kid k, string ex, bool open)
    {
        var b = NB(520, 840); var g = G(b);
        Color skin = k.ghost ? C("#e4ecf0") : C("#f7d3b2");
        Color shirt = k.ghost ? C("#d8e2e8") : C("#f4f3ee");
        Color bottom = k.ghost ? C("#9aaab8") : C("#27365f");
        Color dark = k.ghost ? C("#050508") : C("#2a1e18");
        Color mouthC = C("#6a2420");
        float bw = k.chubby ? 224 : 184, hw = k.chubby ? 318 : 300;
        float L = KCX - bw / 2, Rr = KCX + bw / 2;

        // tóc sau
        if (k.hair == "pigtails")
            foreach (int s in new int[] { -1, 1 })
            {
                EllO(g, k.hairC, OL, 3, KCX + s * 168, 360, 44, 100);
                EllO(g, k.hairC, OL, 3, KCX + s * 160, 270, 34, 34);
            }
        if (k.hair == "bob") FillRR(g, k.hairC, KCX - 162, 150, 324, 250, 90);
        if (k.hair == "long") FillRR(g, k.hairC, KCX - 168, 150, 336, 430, 80);

        // chân
        if (!k.ghost)
        {
            float lw = k.chubby ? 54 : 44;
            foreach (int s in new int[] { -1, 1 })
            {
                float lx = KCX + s * 46 - lw / 2;
                FillRRO(g, skin, OL, 3.5f, lx, 610, lw, 190, 16);
                Rect(g, C("#f4f4f4"), lx + 2, 756, lw - 4, 40);
                EllO(g, C("#2a2422"), OL, 3, lx + lw / 2 + s * 6, 806, 42, 22);
                Ell(g, C("#ffffff", 70), lx + lw / 2 + s * 6 - 10, 798, 12, 5);
            }
        }
        // quần / váy
        if (k.girl)
        {
            PolyO(g, bottom, OL, 3.5f, L + 4, 556, Rr - 4, 556, Rr + 26, 684, L - 26, 684);
            for (int i = 1; i < 5; i++) { float x = L - 20 + (bw + 40) * i / 5f; Ln(g, C("#000000", 50), 3, KCX + (x - KCX) * 0.8f, 566, x, 680); }
        }
        else
        {
            FillRRO(g, bottom, OL, 3.5f, L + 4, 552, bw - 8, 108, 14);
            Ln(g, C("#000000", 70), 3, KCX, 600, KCX, 658);
        }
        // thân áo
        using (var p = RR(L, 392, bw, 190, 44))
        {
            using (var br = new LinearGradientBrush(new RectangleF(L, 391, bw, 192), shirt, Color.FromArgb(255, shirt.R - 30, shirt.G - 30, shirt.B - 26), 0f)) g.FillPath(br, p);
            using (var pen = new Pen(OL, 3.5f)) g.DrawPath(pen, p);
        }
        for (int i = 0; i < 3; i++) Ell(g, C("#b8b8b0"), KCX, 470 + i * 34, 4, 4);
        StrokeRR(g, C("#9a9a90"), 2, KCX + 28, 450, 40, 34, 4);
        PolyO(g, shirt, OL, 2.5f, KCX - 44, 394, KCX - 2, 394, KCX - 8, 428);
        PolyO(g, shirt, OL, 2.5f, KCX + 44, 394, KCX + 2, 394, KCX + 8, 428);
        // khăn quàng đỏ
        Color scarf = k.ghost ? C("#c8a0a8") : C("#d42a2f");
        PolyO(g, scarf, OL, 2.5f, KCX - 8, 432, KCX - 34, 510, KCX - 14, 514, KCX + 2, 440);
        PolyO(g, scarf, OL, 2.5f, KCX + 8, 432, KCX + 30, 500, KCX + 12, 506, KCX - 2, 440);
        PolyO(g, scarf, OL, 2.5f, KCX - 30, 402, KCX + 30, 402, KCX, 442);

        // tay theo tư thế
        string pose = "down";
        if (ex == "so") pose = "chest";
        if (ex == "vui" && (k.id == "mai" || k.id == "linh" || k.id == "minh")) pose = "wave";
        float sLx = L + 20, sRx = Rr - 20, sy = 424;
        if (pose == "chest")
        {
            Arm(g, sLx, sy, L - 22, 520, KCX - 32, 500, shirt, skin, true);
            Arm(g, sRx, sy, Rr + 22, 520, KCX + 32, 500, shirt, skin, false);
        }
        else
        {
            Arm(g, sLx, sy, L - 18, 510, L - 26, 592, shirt, skin, true);
            if (pose == "wave") Arm(g, sRx, sy, Rr + 46, 372, Rr + 62, 286, shirt, skin, false);
            else Arm(g, sRx, sy, Rr + 18, 510, Rr + 26, 592, shirt, skin, false);
        }
        if (k.monitor) Ln(g, C("#d42a2f"), 16, sLx - 9, sy + 34, sLx + 14, sy + 44);

        // cổ + đầu
        Rect(g, skin, KCX - 20, 360, 40, 48);
        foreach (int s in new int[] { -1, 1 }) EllO(g, skin, OL, 3, KCX + s * (hw / 2 - 4), 268, 22, 30);
        EllO(g, skin, OL, 3.5f, KCX, 245, hw / 2, 146);
        if (!k.ghost) { Ell(g, C("#ff8a8a", 80), KCX - 92, 305, 26, 15); Ell(g, C("#ff8a8a", 80), KCX + 92, 305, 26, 15); }

        // lông mày
        Color brow = k.ghost ? C("#30303a") : A(k.hairC, 255);
        float[] e2 = { EX1, EX2 };
        for (int i = 0; i < 2; i++)
        {
            float x = e2[i]; int s = i == 0 ? -1 : 1;
            if (ex == "so") Arc(g, brow, 6, x - 22, 188, 44, 24, 200, 140);
            else if (ex == "buon" || ex == "khoc") Ln(g, brow, 6, x + s * 22, 222, x - s * 14, 208);
            else if (ex == "tram") Ln(g, brow, 6, x - 18, 218, x + 18, 218);
            else if (ex == "vui") Arc(g, brow, 6, x - 20, 200, 40, 20, 200, 140);
            else if (ex != "ma") Arc(g, brow, 6, x - 20, 206, 40, 18, 205, 130);
        }
        // mắt
        foreach (float x in e2)
        {
            if (ex == "vui") Arc(g, dark, 7, x - 18, EY - 10, 36, 30, 180, 180);
            else if (ex == "khoc") Arc(g, dark, 7, x - 17, EY - 16, 34, 22, 0, 180);
            else if (ex == "so")
            {
                EllO(g, C("#ffffff"), dark, 3.5f, x, EY, 22, 26);
                Ell(g, dark, x, EY + 2, 8, 9); Ell(g, C("#ffffff"), x + 3, EY - 2, 3, 3);
            }
            else if (ex == "ma") { Ell(g, C("#000000"), x, EY + 4, 22, 28); Ell(g, C("#ffffff", 110), x, EY + 6, 2.5f, 2.5f); }
            else
            {
                float ry = ex == "buon" ? 17 : 20, oy = ex == "buon" ? 4 : 0;
                Ell(g, dark, x, EY + oy, 15, ry);
                Ell(g, C("#ffffff"), x + 5, EY + oy - (ex == "buon" ? 2 : 8), 5, 6);
                Ell(g, C("#ffffff", 150), x - 5, EY + oy + 8, 2.5f, 2.5f);
                if (ex == "tram")
                {
                    Rect(g, skin, x - 20, EY - 26, 40, 20);
                    Ln(g, dark, 6, x - 17, EY - 6, x + 17, EY - 6);
                }
            }
        }
        if (ex == "khoc")
            foreach (float x in e2)
            {
                using (var br = new LinearGradientBrush(new RectangleF(x - 8, EY - 1, 16, 92), C("#9fd4ff", 210), C("#9fd4ff", 40), 90f))
                    g.FillRectangle(br, x - 6, EY, 12, 90);
                Ell(g, C("#9fd4ff", 200), x, EY + 96, 7, 9);
            }
        // miệng
        float my = 326;
        if (!open)
        {
            if (ex == "vui") Arc(g, mouthC, 6, KCX - 32, my - 26, 64, 36, 15, 150);
            else if (ex == "so") EllO(g, mouthC, OL, 2, KCX, my, 9, 11);
            else if (ex == "buon") Arc(g, mouthC, 5, KCX - 18, my - 2, 36, 20, 205, 130);
            else if (ex == "khoc") Arc(g, mouthC, 6, KCX - 26, my - 6, 52, 26, 205, 130);
            else if (ex == "tram") Ln(g, mouthC, 5, KCX - 14, my, KCX + 14, my);
            else if (ex == "ma") Ell(g, C("#000000"), KCX, my + 4, 8, 4);
            else Arc(g, mouthC, 5, KCX - 20, my - 16, 40, 22, 20, 140);
        }
        else
        {
            if (ex == "vui")
            {
                using (var p = new GraphicsPath())
                {
                    p.AddArc(KCX - 32, my - 30, 64, 56, 0, 180); p.CloseFigure();
                    using (var br = new SolidBrush(mouthC)) g.FillPath(br, p);
                    using (var pen = new Pen(OL, 2.5f)) g.DrawPath(pen, p);
                }
                Ell(g, C("#ff8a90"), KCX, my + 14, 14, 7);
            }
            else if (ex == "so") { EllO(g, mouthC, OL, 2.5f, KCX, my + 4, 15, 21); Ell(g, C("#ff8a90"), KCX, my + 16, 9, 5); }
            else if (ex == "khoc") { EllO(g, mouthC, OL, 2.5f, KCX, my + 4, 24, 17); Ell(g, C("#ff8a90"), KCX, my + 14, 13, 6); }
            else if (ex == "ma") Ell(g, C("#000000"), KCX, my + 10, 14, 24);
            else if (ex == "buon") EllO(g, mouthC, OL, 2, KCX, my + 4, 12, 8);
            else if (ex == "tram") EllO(g, mouthC, OL, 2, KCX, my + 2, 10, 8);
            else { EllO(g, mouthC, OL, 2.5f, KCX, my + 2, 15, 12); Ell(g, C("#ff8a90"), KCX, my + 9, 8, 4); }
        }

        // tóc trước
        if (k.hair == "pigtails")
        {
            HairCap(g, k, 196, hw);
            for (int i = -3; i <= 3; i++) if (i != 0) Ell(g, k.hairC, KCX + i * 40, 192, 26, 22);
            FillRR(g, k.hairC, KCX - hw / 2 - 8, 170, 34, 160, 16); FillRR(g, k.hairC, KCX + hw / 2 - 26, 170, 34, 160, 16);
            foreach (int s in new int[] { -1, 1 })
            {
                float bx = KCX + s * 150, by = 236;
                PolyO(g, k.acc, OL, 2, bx, by, bx - 30, by - 22, bx - 30, by + 22);
                PolyO(g, k.acc, OL, 2, bx, by, bx + 30, by - 22, bx + 30, by + 22);
                EllO(g, k.acc, OL, 2, bx, by, 9, 9);
            }
            Star5(g, C("#ffe070"), KCX + 92, 150, 16);
        }
        else if (k.hair == "bob")
        {
            HairCap(g, k, 206, hw);
            Rect(g, k.hairC, KCX - 118, 140, 236, 66);
            FillRR(g, k.hairC, KCX - hw / 2 - 16, 160, 54, 230, 26); FillRR(g, k.hairC, KCX + hw / 2 - 38, 160, 54, 230, 26);
            FillRRO(g, k.acc, OL, 2, KCX - 116, 168, 46, 18, 8);
        }
        else if (k.hair == "short_boy")
        {
            HairCap(g, k, 170, hw);
            Poly(g, k.hairC, KCX - 146, 150, KCX + 70, 136, KCX - 30, 212, KCX - 122, 196);
            FillRR(g, k.hairC, KCX - hw / 2 - 6, 160, 26, 90, 12); FillRR(g, k.hairC, KCX + hw / 2 - 20, 160, 26, 90, 12);
            Bez(g, k.hairC, 12, KCX + 10, 104, KCX + 20, 60, KCX + 50, 54, KCX + 64, 72);
        }
        else if (k.hair == "buzz")
        {
            HairCap(g, k, 160, hw);
            var rr = new Random(5);
            for (int i = 0; i < 160; i++) Ell(g, C("#5a4a3a", 120), KCX - 140 + rr.Next(280), 98 + rr.Next(60), 1.5f, 1.5f);
        }
        else if (k.hair == "messy")
        {
            HairCap(g, k, 196, hw);
            for (int i = -4; i <= 4; i++) Poly(g, k.hairC, KCX + i * 34 - 24, 186, KCX + i * 34 + 24, 186, KCX + i * 34 + 8, 226 + (Math.Abs(i) % 2) * 16);
            for (int i = -2; i <= 2; i++) Poly(g, k.hairC, KCX + i * 50 - 30, 112, KCX + i * 50 + 30, 112, KCX + i * 50 + 14, 72);
            FillRR(g, k.hairC, KCX - hw / 2 - 8, 160, 30, 110, 14); FillRR(g, k.hairC, KCX + hw / 2 - 22, 160, 30, 110, 14);
        }
        else if (k.hair == "long")
        {
            HairCap(g, k, 236, hw);
            for (int i = -3; i <= 3; i++) Ell(g, k.hairC, KCX + i * 42, 232, 26, 34);
            FillRR(g, k.hairC, KCX - hw / 2 - 18, 170, 58, 300, 26); FillRR(g, k.hairC, KCX + hw / 2 - 40, 170, 58, 300, 26);
        }
        if (k.hair != "long") Arc(g, C("#ffffff", 55), 8, KCX - 110, 110, 150, 70, 200, 70);
        if (k.glasses) Glasses(g);
        g.Dispose();
        if (k.ghost) MulAlphaRows(b, 500, 760);
        return b;
    }
    static void Glasses(Graphics g)
    {
        foreach (float x in new float[] { EX1, EX2 })
        {
            Ell(g, C("#ffffff", 35), x, EY, 33, 31);
            using (var p = new Pen(C("#2a2a2a"), 5)) g.DrawEllipse(p, x - 33, EY - 31, 66, 62);
            Arc(g, C("#ffffff", 120), 3, x - 22, EY - 22, 24, 20, 200, 60);
        }
        Arc(g, C("#2a2a2a"), 5, KCX - 22, EY - 10, 44, 20, 200, 140);
        Ln(g, C("#2a2a2a"), 4, EX1 - 33, EY - 6, EX1 - 82, EY - 10);
        Ln(g, C("#2a2a2a"), 4, EX2 + 33, EY - 6, EX2 + 82, EY - 10);
    }
    static Bitmap DrawBlink(Kid k)
    {
        var b = NB(520, 840); var g = G(b);
        Color skin = C("#f7d3b2");
        foreach (float x in new float[] { EX1, EX2 })
        {
            Ell(g, skin, x, EY + 2, 27, 31);
            Arc(g, C("#2a1e18"), 6, x - 17, EY - 8, 34, 18, 10, 160);
        }
        if (k.glasses) Glasses(g);
        g.Dispose(); return b;
    }

    // --- Bác Thọ ---
    static Bitmap DrawTho(string ex, bool open)
    {
        var b = NB(600, 1060); var g = G(b); var r = new Random(3);
        float cx = 300;
        Color skin = C("#d9a47c"), shirt = C("#8b8a55"), shirtD = C("#6f6e42"), dark = C("#2a1e18");
        foreach (int s in new int[] { -1, 1 })
        {
            FillRRO(g, C("#5f5d3c"), OL, 3.5f, cx + (s < 0 ? -80 : 10), 650, 70, 350, 18);
            EllO(g, C("#3a2616"), OL, 3, cx + s * 45, 1012, 50, 20);
        }
        using (var p = RR(cx - 128, 368, 256, 312, 60))
        {
            using (var br = new LinearGradientBrush(new RectangleF(cx - 129, 368, 258, 312), shirt, shirtD, 0f)) g.FillPath(br, p);
            using (var pen = new Pen(OL, 3.5f)) g.DrawPath(pen, p);
        }
        Rect(g, C("#3b2f22"), cx - 126, 640, 252, 26); FillRR(g, C("#c9a64a"), cx - 18, 642, 36, 22, 4);
        FillRRO(g, shirtD, OL, 2, cx - 104, 440, 70, 60, 8); FillRRO(g, shirtD, OL, 2, cx + 34, 440, 70, 60, 8);
        Ln(g, OL, 2, cx - 104, 458, cx - 34, 458); Ln(g, OL, 2, cx + 34, 458, cx + 104, 458);
        EllO(g, C("#d9b440"), OL, 2, cx - 68, 420, 11, 11);
        for (int i = 0; i < 5; i++) Ell(g, C("#3a3a22"), cx, 410 + i * 50, 5, 5);
        FillRR(g, C("#5e5d36"), cx - 126, 378, 70, 22, 6); FillRR(g, C("#5e5d36"), cx + 56, 378, 70, 22, 6);
        PolyO(g, shirt, OL, 2.5f, cx - 52, 372, cx - 4, 372, cx - 14, 414);
        PolyO(g, shirt, OL, 2.5f, cx + 52, 372, cx + 4, 372, cx + 14, 414);
        // tay trái
        Ln(g, OL, 50, cx - 112, 404, cx - 150, 535); Ln(g, OL, 50, cx - 150, 535, cx - 158, 640);
        Ln(g, shirt, 42, cx - 112, 404, cx - 150, 535); Ln(g, shirt, 42, cx - 150, 535, cx - 158, 640);
        EllO(g, skin, OL, 3.5f, cx - 158, 660, 26, 26);
        bool bottle = ex == "normal" || ex == "say";
        if (bottle)
        {
            Ln(g, OL, 50, cx + 112, 404, cx + 160, 520); Ln(g, OL, 50, cx + 160, 520, cx + 142, 600);
            Ln(g, shirt, 42, cx + 112, 404, cx + 160, 520); Ln(g, shirt, 42, cx + 160, 520, cx + 142, 600);
            FillRRO(g, C("#2f6b3a", 235), OL, 2.5f, cx + 122, 560, 42, 116, 10);
            FillRRO(g, C("#2f6b3a", 235), OL, 2.5f, cx + 135, 516, 16, 48, 4);
            Rect(g, C("#d8c890"), cx + 124, 600, 38, 30);
            Ln(g, C("#ffffff", 90), 4, cx + 132, 570, cx + 132, 660);
            EllO(g, skin, OL, 3.5f, cx + 143, 612, 26, 26);
        }
        else if (ex == "hien")
        {
            Ln(g, OL, 50, cx + 112, 404, cx + 150, 535); Ln(g, OL, 50, cx + 150, 535, cx + 158, 640);
            Ln(g, shirt, 42, cx + 112, 404, cx + 150, 535); Ln(g, shirt, 42, cx + 150, 535, cx + 158, 640);
            EllO(g, skin, OL, 3.5f, cx + 158, 660, 26, 26);
        }
        // đầu
        Rect(g, skin, cx - 36, 326, 72, 64);
        foreach (int s in new int[] { -1, 1 }) EllO(g, skin, OL, 3, cx + s * 96, 258, 18, 28);
        EllO(g, skin, OL, 3.5f, cx, 245, 98, 120);
        for (int i = 0; i < 380; i++)
        {
            double a = r.NextDouble() * Math.PI; float rr = 0.55f + (float)r.NextDouble() * 0.42f;
            float x = cx + (float)Math.Cos(a) * 92 * rr, y = 255 + (float)Math.Sin(a) * 110 * rr;
            if (y > 292) Ell(g, C("#6b6460", 110), x, y, 1.4f, 1.4f);
        }
        Ell(g, C("#9a958c"), cx - 90, 210, 14, 40); Ell(g, C("#9a958c"), cx + 90, 210, 14, 40);
        // mũ bảo vệ
        FillRRO(g, C("#6f6e40"), OL, 3, cx - 106, 100, 212, 94, 44);
        Rect(g, C("#4a4a2a"), cx - 108, 168, 216, 24);
        using (var p = new GraphicsPath())
        {
            p.AddArc(cx - 112, 168, 224, 50, 0, 180); p.CloseFigure();
            using (var br = new SolidBrush(C("#2e2e1c"))) g.FillPath(br, p);
        }
        EllO(g, C("#d9b440"), OL, 2, cx, 138, 17, 17); Ell(g, C("#b3241f"), cx, 138, 7, 7);
        // lông mày
        Color brow = C("#7a756c");
        if (ex == "khoc") { Ln(g, brow, 9, cx - 76, 226, cx - 16, 208); Ln(g, brow, 9, cx + 76, 226, cx + 16, 208); }
        else if (ex == "hien") { Arc(g, brow, 9, cx - 76, 206, 58, 20, 200, 140); Arc(g, brow, 9, cx + 18, 206, 58, 20, 200, 140); }
        else if (ex == "say") { Ln(g, brow, 9, cx - 76, 214, cx - 16, 222); Ln(g, brow, 9, cx + 76, 206, cx + 16, 216); }
        else { Ln(g, brow, 9, cx - 76, 212, cx - 16, 222); Ln(g, brow, 9, cx + 76, 212, cx + 16, 222); }
        // kính đen (mù)
        foreach (int s in new int[] { -1, 1 })
        {
            EllO(g, C("#111111", 248), C("#000000"), 4, cx + s * 42, 252, 32, 29);
            Arc(g, C("#ffffff", 80), 3, cx + s * 42 - 20, 232, 22, 18, 200, 70);
        }
        Ln(g, C("#000000"), 5, cx - 12, 250, cx + 12, 250);
        Ln(g, C("#000000"), 4, cx - 74, 248, cx - 94, 244); Ln(g, C("#000000"), 4, cx + 74, 248, cx + 94, 244);
        Ell(g, C("#c48a60"), cx, 290, 15, 11); Arc(g, C("#8a5a3a"), 3, cx - 14, 284, 28, 14, 20, 140);
        if (ex == "say" || ex == "khoc") { Ell(g, C("#e05a4a", 90), cx - 64, 300, 24, 14); Ell(g, C("#e05a4a", 90), cx + 64, 300, 24, 14); Ell(g, C("#e05a4a", 70), cx, 290, 18, 12); }
        Ell(g, C("#8f8a80"), cx - 20, 314, 25, 9); Ell(g, C("#8f8a80"), cx + 20, 314, 25, 9);
        float my = 338; Color mc = C("#5a1f18");
        if (!open)
        {
            if (ex == "say") Bez(g, mc, 5, cx - 22, my, cx - 8, my - 6, cx + 6, my + 6, cx + 22, my - 2);
            else if (ex == "khoc") Arc(g, mc, 6, cx - 26, my - 4, 52, 22, 205, 130);
            else if (ex == "hien") Arc(g, mc, 5, cx - 22, my - 18, 44, 22, 20, 140);
            else Arc(g, mc, 5, cx - 20, my - 2, 40, 16, 205, 130);
        }
        else
        {
            if (ex == "say") EllO(g, mc, OL, 2, cx + 4, my + 4, 18, 13);
            else if (ex == "khoc") EllO(g, mc, OL, 2, cx, my + 8, 24, 18);
            else if (ex == "hien") { using (var p = new GraphicsPath()) { p.AddArc(cx - 22, my - 16, 44, 36, 0, 180); p.CloseFigure(); using (var br = new SolidBrush(mc)) g.FillPath(br, p); } }
            else EllO(g, mc, OL, 2, cx, my + 4, 16, 10);
        }
        if (ex == "khoc")
        {
            foreach (int s in new int[] { -1, 1 })
            {
                using (var br = new LinearGradientBrush(new RectangleF(cx + s * 42 - 8, 279, 16, 102), C("#9fd4ff", 220), C("#9fd4ff", 40), 90f))
                    g.FillRectangle(br, cx + s * 42 - 6, 280, 12, 100);
                Ell(g, C("#9fd4ff", 200), cx + s * 42, 386, 7, 9);
            }
            Ln(g, OL, 50, cx + 112, 404, cx + 150, 520); Ln(g, OL, 50, cx + 150, 520, cx + 70, 330);
            Ln(g, shirt, 42, cx + 112, 404, cx + 150, 520); Ln(g, shirt, 42, cx + 150, 520, cx + 70, 330);
            EllO(g, skin, OL, 3.5f, cx + 64, 312, 26, 26);
        }
        g.Dispose(); return b;
    }

    // ================================================================ ITEMS
    static Bitmap Icon(string id)
    {
        var b = NB(128, 128); var g = G(b); var r = new Random(id.GetHashCode());
        switch (id)
        {
            case "vong_minh":
            case "vong_chay_1":
            case "vong_chay_2":
                {
                    bool burnt = id != "vong_minh";
                    using (var p = new Pen(C(burnt ? "#2a1a10" : "#8a7a6a"), 2)) g.DrawEllipse(p, 24, 28, 80, 72);
                    for (int i = 0; i < 12; i++)
                    {
                        double a = i * Math.PI / 6;
                        float x = 64 + (float)Math.Cos(a) * 40, y = 64 + (float)Math.Sin(a) * 36;
                        Color c = burnt ? (i % 2 == 0 ? C("#4a1c10") : C("#1f2a16")) : (i % 2 == 0 ? C("#d83a3a") : C("#3aa860"));
                        EllO(g, c, C("#1a1010"), 1.5f, x, y, burnt ? 9 + r.Next(3) : 9, burnt ? 8 : 9);
                        Ell(g, C("#ffffff", burnt ? 40 : 140), x - 3, y - 3, 3, 3);
                    }
                    if (burnt) { Glow(g, 64, 64, 60, 50, C("#000000", 90)); Ell(g, C("#ff7a2a", 160), 40, 90, 2, 2); }
                    if (id == "vong_chay_2") Txt(g, "LINH", "Segoe UI", 18, FontStyle.Bold, C("#d8c0a0"), 64, 52, true);
                    break;
                }
            case "giay_mai":
                PolyO(g, C("#fbf6e6"), C("#8a7a5a"), 2, 18, 30, 104, 18, 112, 98, 26, 110);
                for (int i = 0; i < 4; i++) Ln(g, C("#6a8ac8", 150), 2, 30, 44 + i * 14, 98, 36 + i * 14);
                Txt(g, "♥", "Segoe UI Symbol", 26, FontStyle.Bold, C("#ff6fa5"), 84, 70, true);
                break;
            case "dong_xu":
                EllO(g, C("#b8893a"), C("#5a3a10"), 3, 64, 64, 50, 50);
                using (var p = new Pen(C("#e0b860"), 3)) g.DrawEllipse(p, 22, 22, 84, 84);
                EllO(g, C("#f2ede0"), C("#1a1a1a"), 2, 64, 64, 28, 28);
                using (var br = new SolidBrush(C("#1a1a1a")))
                {
                    g.FillPie(br, 36, 36, 56, 56, 90, 180);
                    g.FillEllipse(new SolidBrush(C("#f2ede0")), 50, 36, 28, 28);
                    g.FillEllipse(br, 50, 64, 28, 28);
                }
                Ell(g, C("#1a1a1a"), 64, 50, 5, 5); Ell(g, C("#f2ede0"), 64, 78, 5, 5);
                break;
            case "chia_tai_vu":
                using (var p = new Pen(C("#b0a090"), 4)) g.DrawEllipse(p, 14, 14, 34, 34);
                using (var p = new Pen(C("#c8a24a"), 7)) g.DrawEllipse(p, 34, 30, 30, 30);
                Ln(g, C("#c8a24a"), 8, 60, 56, 104, 100); Ln(g, C("#c8a24a"), 6, 92, 88, 100, 80); Ln(g, C("#c8a24a"), 6, 100, 96, 108, 88);
                FillRRO(g, C("#efe8d8"), C("#7a6a50"), 2, 14, 74, 54, 32, 4);
                Txt(g, "TÀI VỤ", "Segoe UI", 12, FontStyle.Bold, C("#5a1a10"), 41, 82, true);
                Glow(g, 64, 104, 12, 10, C("#2a1a0a", 220));
                break;
            case "so_tai_vu":
                FillRRO(g, C("#2a5a9a"), C("#102040"), 2, 26, 16, 78, 98, 6);
                Rect(g, C("#1a3a6a"), 26, 16, 12, 98);
                FillRR(g, C("#efe8d8"), 46, 38, 48, 26, 3);
                Txt(g, "SỔ CHI", "Segoe UI", 12, FontStyle.Bold, C("#1a2a4a"), 70, 42, true);
                Rect(g, C("#f4efe0"), 102, 20, 4, 90);
                break;
            case "bai_bao":
                PolyO(g, C("#e4ddc8"), C("#6a6050"), 2, 16, 24, 106, 18, 112, 104, 22, 110);
                Rect(g, C("#2a2a2a"), 26, 30, 76, 10);
                for (int i = 0; i < 6; i++) Ln(g, C("#5a5a5a", 160), 2, 28, 52 + i * 9, i % 2 == 0 ? 68 : 100, 51 + i * 9);
                Rect(g, C("#8a8478"), 74, 50, 26, 22);
                break;
            case "la_bua":
                FillRRO(g, C("#f2c83a"), C("#8a6a10"), 2, 40, 8, 48, 112, 3);
                Bez(g, C("#c81818"), 4, 64, 18, 50, 34, 78, 40, 64, 54);
                Bez(g, C("#c81818"), 4, 52, 60, 76, 62, 52, 78, 74, 84);
                Ln(g, C("#c81818"), 4, 64, 84, 64, 110); Ln(g, C("#c81818"), 3, 54, 98, 74, 98);
                Ell(g, C("#c81818"), 64, 28, 4, 4);
                break;
            case "chia_bang_dien":
                Bez(g, C("#141414"), 5, 20, 30, 50, 10, 30, 60, 54, 56);
                Glow(g, 20, 30, 10, 10, C("#000000", 200));
                using (var p = new Pen(C("#a8a8b0"), 6)) g.DrawEllipse(p, 50, 46, 26, 26);
                Ln(g, C("#a8a8b0"), 7, 72, 70, 104, 102); Ln(g, C("#a8a8b0"), 5, 92, 90, 98, 84);
                break;
            case "ban_kiem_diem":
                PolyO(g, C("#fbfaf4"), C("#7a7a7a"), 2, 22, 14, 104, 14, 104, 114, 22, 114);
                Txt(g, "BẢN KIỂM ĐIỂM", "Segoe UI", 10, FontStyle.Bold, C("#2a2a2a"), 63, 20, true);
                for (int i = 0; i < 6; i++) { Ln(g, C("#9ab0d8", 160), 1, 28, 42 + i * 11, 98, 42 + i * 11); Bez(g, C("#2a3a8a", 180), 1.5f, 30, 40 + i * 11, 50, 36 + i * 11, 70, 44 + i * 11, 90 - (i % 3) * 10, 39 + i * 11); }
                Ell(g, C("#d83a3a", 120), 86, 100, 10, 10);
                break;
            case "chu_van":
                FillRRO(g, C("#a8743a"), C("#4a2a10"), 3, 18, 18, 92, 92, 10);
                for (int i = 0; i < 5; i++) Ln(g, C("#8a5a28", 120), 2, 22, 30 + i * 18, 106, 34 + i * 18);
                using (var p = RP(C("#3a1a08"), 9))
                {
                    g.DrawLine(p, 64, 34, 64, 94); g.DrawLine(p, 34, 64, 94, 64);
                    g.DrawLine(p, 64, 34, 40, 34); g.DrawLine(p, 34, 64, 34, 88);
                    g.DrawLine(p, 64, 94, 88, 94); g.DrawLine(p, 94, 64, 94, 40);
                }
                break;
            case "den":
                Glow(g, 64, 34, 40, 40, C("#ffb040", 120));
                Ell(g, C("#ffd36a"), 64, 36, 7, 14); Ell(g, C("#fff6d0"), 64, 40, 3, 6);
                PolyO(g, C("#c8a24a"), C("#5a3a10"), 2, 34, 56, 94, 56, 82, 76, 46, 76);
                Rect(g, C("#a8823a"), 58, 76, 12, 22);
                FillRRO(g, C("#c8a24a"), C("#5a3a10"), 2, 38, 96, 52, 14, 4);
                break;
            case "huong":
                for (int i = 0; i < 3; i++)
                {
                    float x = 50 + i * 14;
                    Ln(g, C("#8a3a1a"), 3, x, 66, x + (i - 1) * 4, 22);
                    Ell(g, C("#ff4a1a"), x + (i - 1) * 4, 22, 3, 3);
                    Bez(g, C("#d0d0d8", 110), 2, x + (i - 1) * 4, 20, x + 10, 12, x - 8, 6, x + 4, 0);
                }
                using (var p = new GraphicsPath())
                {
                    p.AddArc(28, 50, 72, 56, 0, 180); p.CloseFigure();
                    using (var br = new SolidBrush(C("#8a2a1a"))) g.FillPath(br, p);
                }
                Rect(g, C("#c8a24a"), 28, 74, 72, 5);
                Ell(g, C("#5a1a10"), 64, 78, 36, 6);
                break;
        }
        g.Dispose(); return b;
    }

    // ================================================================ UI & FX
    static void UI()
    {
        // khung thoại
        var b = NB(W, 278); var g = G(b);
        VGrad(g, 0, 0, W, 70, C("#0b0807", 0), C("#0b0807", 215));
        Rect(g, C("#0b0807", 215), 0, 70, W, 208);
        HGrad(g, 0, 34, W / 2, 3, C("#c9a86a", 0), C("#c9a86a", 200));
        HGrad(g, W / 2, 34, W / 2, 3, C("#c9a86a", 200), C("#c9a86a", 0));
        Poly(g, C("#c9a86a"), 960, 24, 972, 36, 960, 48, 948, 36);
        Poly(g, C("#c9a86a", 160), 920, 30, 926, 36, 920, 42, 914, 36); Poly(g, C("#c9a86a", 160), 1000, 30, 1006, 36, 1000, 42, 994, 36);
        g.Dispose(); Save(b, "gui/textbox.png");

        b = NB(340, 64); g = G(b);
        using (var p = RR(2, 2, 336, 60, 14))
        {
            using (var br = new LinearGradientBrush(new RectangleF(0, 0, 340, 64), C("#6b2420"), C("#3a1210"), 90f)) g.FillPath(br, p);
            using (var pen = new Pen(C("#d8b878"), 2.5f)) g.DrawPath(pen, p);
        }
        g.Dispose(); Save(b, "gui/namebox.png");

        b = NB(240, 240); g = G(b);
        using (var p = RR(3, 3, 234, 234, 20))
        {
            using (var br = new LinearGradientBrush(new RectangleF(0, 0, 240, 240), C("#231a14", 245), C("#120d0a", 245), 90f)) g.FillPath(br, p);
            using (var pen = new Pen(C("#a88a58"), 3)) g.DrawPath(pen, p);
        }
        StrokeRR(g, C("#a88a58", 70), 1.5f, 9, 9, 222, 222, 16);
        g.Dispose(); Save(b, "gui/hns_panel.png");

        b = NB(240, 240); g = G(b);
        using (var p = RR(3, 3, 234, 234, 16))
        {
            using (var br = new LinearGradientBrush(new RectangleF(0, 0, 240, 240), C("#f2e8cc"), C("#d8c8a0"), 90f)) g.FillPath(br, p);
            using (var pen = new Pen(C("#7a5a30"), 3)) g.DrawPath(pen, p);
        }
        var rp = new Random(3);
        for (int i = 0; i < 400; i++) Ell(g, C("#8a6a3a", 30), 10 + rp.Next(220), 10 + rp.Next(220), 2, 2);
        g.Dispose(); Save(b, "gui/hns_paper.png");

        string[] bn = { "idle", "hover", "selected", "insensitive" };
        string[] bf = { "#2a1d16", "#6a2a1e", "#5a4320", "#1a1512" };
        string[] bo = { "#8a6a40", "#f0c878", "#ffd88a", "#4a4038" };
        for (int i = 0; i < 4; i++)
        {
            b = NB(120, 60); g = G(b);
            using (var p = RR(2, 2, 116, 56, 12))
            {
                using (var br = new LinearGradientBrush(new RectangleF(0, 0, 120, 60), C(bf[i]), Color.FromArgb(255, C(bf[i]).R / 2, C(bf[i]).G / 2, C(bf[i]).B / 2), 90f)) g.FillPath(br, p);
                using (var pen = new Pen(C(bo[i]), 2.5f)) g.DrawPath(pen, p);
            }
            g.Dispose(); Save(b, "gui/hns_btn_" + bn[i] + ".png");
        }
        for (int i = 0; i < 3; i++)
        {
            b = NB(120, 120); g = G(b);
            if (i == 1) Glow(g, 60, 60, 64, 64, C("#ffd88a", 70));
            FillRRO(g, C("#120d0a", 225), C(i == 0 ? "#7a5f3c" : (i == 1 ? "#ffd88a" : "#ff9a6a")), i == 0 ? 2.5f : 3.5f, 6, 6, 108, 108, 14);
            g.Dispose(); Save(b, "gui/hns_slot_" + (i == 0 ? "idle" : (i == 1 ? "hover" : "selected")) + ".png");
        }
        b = NB(120, 120); g = G(b);
        for (int k = 0; k < 3; k++) StrokeRR(g, C("#ffe8a0", 50 + k * 60), 7 - k * 2, 8 + k * 2, 8 + k * 2, 104 - k * 4, 104 - k * 4, 18);
        FillRR(g, C("#ffe8a0", 26), 12, 12, 96, 96, 16);
        g.Dispose(); Save(b, "gui/hs_hover.png");

        // FX
        b = NB(64, 64); g = G(b);
        Glow(g, 32, 32, 30, 30, C("#ffe8a0", 150));
        Poly(g, C("#fff8e0"), 32, 4, 36, 28, 60, 32, 36, 36, 32, 60, 28, 36, 4, 32, 28, 28);
        g.Dispose(); Save(b, "images/fx/sparkle.png");
        b = NB(4, 80); g = G(b); VGrad(g, 0, 0, 4, 80, C("#b8c8e8", 0), C("#b8c8e8", 150)); g.Dispose(); Save(b, "images/fx/rain.png");
        b = NB(14, 14); g = G(b); Glow(g, 7, 7, 7, 7, C("#fff8e8", 200)); g.Dispose(); Save(b, "images/fx/dust.png");
        b = NB(14, 14); g = G(b); Glow(g, 7, 7, 7, 7, C("#ff9a3a", 255)); Ell(g, C("#ffe0a0"), 7, 7, 1.5f, 1.5f); g.Dispose(); Save(b, "images/fx/ember.png");
        b = NB(60, 60); g = G(b); Glow(g, 30, 30, 30, 30, C("#b8ecff", 200)); Ell(g, C("#ffffff", 220), 30, 30, 3, 3); g.Dispose(); Save(b, "images/fx/wisp.png");
        b = NB(30, 20); g = G(b); Ell(g, C("#5a9a40"), 15, 10, 13, 7); Ln(g, C("#3a6a28"), 1.5f, 3, 10, 27, 10); g.Dispose(); Save(b, "images/fx/leaf.png");
        b = NB(3840, 560); g = G(b);
        var rf = new Random(91);
        for (int i = 0; i < 70; i++)
        {
            float x = (float)rf.NextDouble() * 1920, y = 120 + (float)rf.NextDouble() * 380, rx = 160 + (float)rf.NextDouble() * 260, ry = 50 + (float)rf.NextDouble() * 90;
            for (int k = -1; k <= 2; k++) Glow(g, x + k * 1920, y, rx, ry, C("#d8e0f0", 34));
        }
        g.Dispose(); Save(b, "images/fx/fog.png");
        b = NB(700, 700); g = G(b);
        for (int i = 0; i < 14; i++) Glow(g, 200 + rf.Next(300), 200 + rf.Next(300), 140 + rf.Next(120), 120 + rf.Next(100), C("#9a9aa0", 40));
        g.Dispose(); Save(b, "images/fx/smoke.png");
        b = Flames(5); Save(b, "images/fx/lua1.png"); b = Flames(9); Save(b, "images/fx/lua2.png");
        b = Flowers(); Save(b, "images/fx/hoa.png");
        // đèn pin
        b = NB(3840, 2160); g = G(b);
        g.Clear(Color.FromArgb(238, 0, 0, 4));
        g.CompositingMode = CompositingMode.SourceCopy;
        using (var p = new GraphicsPath())
        {
            p.AddEllipse(1920 - 420, 1080 - 420, 840, 840);
            using (var pb = new PathGradientBrush(p))
            {
                pb.CenterPoint = new PointF(1920, 1080);
                pb.CenterColor = Color.FromArgb(0, 20, 14, 0);
                pb.SurroundColors = new Color[] { Color.FromArgb(238, 0, 0, 4) };
                var bl = new Blend(); bl.Factors = new float[] { 0f, 0.6f, 1f, 1f }; bl.Positions = new float[] { 0f, 0.35f, 0.6f, 1f }; pb.Blend = bl;
                g.FillPath(pb, p);
            }
        }
        g.Dispose(); Save(b, "images/fx/flashlight.png");
        // cánh tay luồn qua ô cửa
        b = NB(1100, 240); g = G(b);
        Ln(g, OL, 70, 0, 150, 700, 120); Ln(g, C("#f4f3ee"), 62, 0, 150, 700, 120);
        Ln(g, OL, 44, 700, 120, 1000, 110); Ln(g, C("#f7d3b2"), 36, 700, 120, 1000, 110);
        Ell(g, C("#d83a3a"), 930, 98, 6, 6); Ell(g, C("#3aa860"), 930, 112, 6, 6); Ell(g, C("#d83a3a"), 930, 126, 6, 6);
        EllO(g, C("#f7d3b2"), OL, 3, 1020, 110, 30, 26);
        for (int k = 0; k < 4; k++) { Ln(g, OL, 15, 1030, 96 + k * 10, 1080, 84 + k * 13); Ln(g, C("#f7d3b2"), 10, 1030, 96 + k * 10, 1080, 84 + k * 13); }
        g.Dispose(); Save(b, "images/fx/tay.png");
        b = NB(240, 360); g = G(b);
        Glow(g, 120, 160, 110, 160, C("#9fc0d8", 50));
        Ln(g, C("#c8d8e0", 220), 34, 120, 360, 120, 200);
        Ell(g, C("#c8d8e0", 230), 120, 180, 30, 34);
        for (int k = 0; k < 4; k++) Ln(g, C("#c8d8e0", 230), 10, 100 + k * 13, 160, 92 + k * 18, 90 - (k == 1 || k == 2 ? 14 : 0));
        Ln(g, C("#c8d8e0", 230), 10, 146, 186, 172, 160);
        for (int k = 0; k < 4; k++) Ell(g, C("#2a2a3a", 200), 92 + k * 18, 92 - (k == 1 || k == 2 ? 14 : 0), 3, 4);
        g.Dispose(); Save(b, "images/fx/tay_ma.png");
    }

    // ================================================================ RUN
    public static void Run(string root)
    {
        Root = root;
        Console.WriteLine("Backgrounds...");
        Save(BgCong(false), "images/bg/cong.png");
        Save(BgLop(), "images/bg/lop.png");
        Save(BgSan(true), "images/bg/san.png");
        Save(BgSan(false), "images/bg/sang.png");
        Save(BgBaoVeCua(), "images/bg/baove_cua.png");
        Save(BgTaiVu(), "images/bg/taivu.png");
        Save(BgBiMat(false), "images/bg/bimat.png");
        Save(BgBiMat(true), "images/bg/phongle.png");
        Save(BgUMinh(), "images/bg/uminh.png");

        Console.WriteLine("Menu...");
        var m = BgCong(true); var g = G(m);
        HGrad(g, 0, 0, W, H, C("#000000", 200), C("#000000", 40));
        Glow(g, 1380, 330, 520, 160, C("#8a0a0a", 90));
        Txt(g, "TRỐN TÌM", "Segoe UI Black", 170, FontStyle.Regular, C("#000000", 160), 1388, 218, true);
        Txt(g, "TRỐN TÌM", "Segoe UI Black", 170, FontStyle.Regular, C("#efe2c8"), 1380, 210, true);
        Txt(g, "Một ván trốn tìm vẫn chưa ai đếm xong...", "Segoe UI", 34, FontStyle.Italic, C("#d8c0a0", 220), 1380, 430, true);
        g.Dispose(); Save(m, "gui/main_menu.png");
        m = BgCong(false); g = G(m); Rect(g, C("#000000", 190), 0, 0, W, H); g.Dispose(); Save(m, "gui/game_menu.png");

        Console.WriteLine("Characters...");
        var kids = new List<Kid>();
        kids.Add(new Kid { id = "mai", girl = true, hair = "pigtails", hairC = C("#1e1512"), acc = C("#ff6fa5"), monitor = true });
        kids.Add(new Kid { id = "minh", girl = false, hair = "short_boy", hairC = C("#1a1410"), acc = C("#ff6fa5"), monitor = true });
        kids.Add(new Kid { id = "tung", girl = false, hair = "buzz", hairC = C("#2a2018"), acc = C("#ffffff"), chubby = true });
        kids.Add(new Kid { id = "linh", girl = true, hair = "bob", hairC = C("#3a2216"), acc = C("#ffcc33") });
        kids.Add(new Kid { id = "khoa", girl = false, hair = "messy", hairC = C("#15110f"), acc = C("#ffffff"), glasses = true });
        string[] exs = { "normal", "vui", "so", "buon", "khoc", "tram" };
        foreach (var k in kids)
        {
            foreach (var e in exs)
            {
                Save(DrawKid(k, e, false), "images/char/" + k.id + "_" + e + "_0.png");
                Save(DrawKid(k, e, true), "images/char/" + k.id + "_" + e + "_1.png");
            }
            Save(DrawBlink(k), "images/char/" + k.id + "_blink.png");
        }
        var ghost = new Kid { id = "ma", girl = true, hair = "long", hairC = C("#0b0b0e"), acc = C("#ffffff"), ghost = true };
        Save(DrawKid(ghost, "ma", false), "images/char/ma.png");
        Save(DrawKid(ghost, "ma", true), "images/char/ma_het.png");
        foreach (var e in new string[] { "normal", "say", "khoc", "hien" })
        {
            Save(DrawTho(e, false), "images/char/tho_" + e + "_0.png");
            Save(DrawTho(e, true), "images/char/tho_" + e + "_1.png");
        }
        Console.WriteLine("Items...");
        foreach (var id in new string[] { "vong_minh", "giay_mai", "dong_xu", "chia_tai_vu", "so_tai_vu", "bai_bao", "la_bua", "chia_bang_dien", "vong_chay_1", "ban_kiem_diem", "vong_chay_2", "chu_van", "den", "huong" })
            Save(Icon(id), "images/items/" + id + ".png");
        Console.WriteLine("UI & FX...");
        UI();
        Console.WriteLine("DONE");
    }
}
