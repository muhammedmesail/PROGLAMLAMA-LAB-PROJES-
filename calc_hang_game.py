"""
Calc & Hang — İşlem Yap, Harfi Kurtar
Kocaeli Sağlık ve Teknoloji Üniversitesi
Programlama Lab I - Proje 1
"""

import random
import json
import os
from datetime import datetime

# Renkli terminal çıktısı için ANSI kodları
class Colors:
    """Terminal renk kodları"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Kelime kategorileri
WORD_CATEGORIES = {
    'meyve': ['elma', 'armut', 'muz', 'kiraz', 'üzüm', 'portakal', 'kavun', 'karpuz', 'çilek', 'mandalina'],
    'hayvan': ['aslan', 'kaplan', 'fil', 'zürafa', 'kanguru', 'köpek', 'kedi', 'tavşan', 'kuş', 'balık'],
    'teknoloji': ['bilgisayar', 'telefon', 'tablet', 'klavye', 'fare', 'monitör', 'yazıcı', 'tarayıcı', 'kamera', 'robot']
}

# Asmaca görselleri
HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    """
]

class CalcHangGame:
    """Calc & Hang oyun sınıfı"""
    
    def __init__(self):
        """Oyun başlangıç ayarları"""
        self.max_errors = 6
        self.reset_game()
    
    def reset_game(self):
        """Oyun değişkenlerini sıfırla"""
        # Rastgele kategori ve kelime seç
        self.category = random.choice(list(WORD_CATEGORIES.keys()))
        self.word = random.choice(WORD_CATEGORIES[self.category]).upper()
        
        # Oyun durumu
        self.guessed_letters = set()
        self.error_count = 0
        self.bonus_points = 0
        self.score = 0
        self.hint_used = False
        
        # Kullanılan işlemler (her işlem 1 kez kullanılabilir)
        self.used_operations = {
            'toplama': False,
            'çıkarma': False,
            'çarpma': False,
            'bölme': False
        }
        
        # Maskelenmiş kelime
        self.masked_word = ['_'] * len(self.word)
    
    def display_game_state(self):
        """Oyun durumunu ekrana yazdır"""
        os.system('clear' if os.name == 'posix' else 'cls')  # Ekranı temizle
        
        print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}║   CALC & HANG — İŞLEM YAP, HARFİ KURTAR      ║{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}╚════════════════════════════════════════════════╝{Colors.END}\n")
        
        # Asmaca görseli
        print(f"{Colors.FAIL}{HANGMAN_STAGES[self.error_count]}{Colors.END}")
        
        # Oyun bilgileri
        print(f"{Colors.CYAN}Kelime: {Colors.BOLD}{' '.join(self.masked_word)}{Colors.END}")
        print(f"{Colors.BLUE}Tahmin edilen harfler: {Colors.END}{', '.join(sorted(self.guessed_letters)) if self.guessed_letters else 'Yok'}")
        print(f"{Colors.WARNING}Kalan hata hakkı: {Colors.BOLD}{self.max_errors - self.error_count}{Colors.END}")
        print(f"{Colors.GREEN}Bonus puan: {Colors.BOLD}{self.bonus_points}{Colors.END}")
        print(f"{Colors.GREEN}Toplam skor: {Colors.BOLD}{self.score}{Colors.END}")
        
        # Kullanılan işlemler
        ops_status = []
        for op, used in self.used_operations.items():
            status = f"{Colors.FAIL}✗{Colors.END}" if used else f"{Colors.GREEN}✓{Colors.END}"
            ops_status.append(f"{op.capitalize()}: {status}")
        print(f"\n{Colors.BLUE}İşlem Durumu:{Colors.END} {' | '.join(ops_status)}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}\n")
    
    def guess_letter(self, letter):
        """Harf tahmini yap"""
        letter = letter.upper()
        
        # Harf kontrolü
        if len(letter) != 1:
            return False, "Lütfen sadece bir harf girin!"
        
        if not letter.isalpha():
            return False, "Lütfen geçerli bir harf girin!"
        
        if letter in self.guessed_letters:
            return False, "Bu harfi zaten tahmin ettiniz!"
        
        # Harfi kaydet
        self.guessed_letters.add(letter)
        
        # Harf kelimede var mı?
        if letter in self.word:
            # Harfi aç
            for i, char in enumerate(self.word):
                if char == letter:
                    self.masked_word[i] = letter
            self.score += 10
            return True, f"{Colors.GREEN}Doğru! '{letter}' harfi kelimede var.{Colors.END}"
        else:
            self.error_count += 1
            self.score -= 5
            return False, f"{Colors.FAIL}Yanlış! '{letter}' harfi kelimede yok.{Colors.END}"
    
    def calculate(self):
        """Hesap makinesi fonksiyonu"""
        print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
        print(f"{Colors.BOLD}HESAP MAKİNESİ{Colors.END}")
        print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
        
        # Kullanılabilir işlemleri göster
        available_ops = [op for op, used in self.used_operations.items() if not used]
        
        if not available_ops:
            print(f"{Colors.FAIL}Tüm işlemler kullanıldı!{Colors.END}")
            input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
            return
        
        print(f"{Colors.GREEN}Kullanılabilir işlemler:{Colors.END}")
        for i, op in enumerate(available_ops, 1):
            print(f"  {i}. {op.capitalize()}")
        print(f"  0. İptal")
        
        # İşlem seçimi
        try:
            choice = input(f"\n{Colors.BLUE}İşlem seçin (1-{len(available_ops)}, 0=iptal):{Colors.END} ").strip()
            
            if choice == '0' or choice.lower() == 'iptal':
                print(f"{Colors.WARNING}İşlem iptal edildi.{Colors.END}")
                input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
                return
            
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(available_ops):
                print(f"{Colors.FAIL}Geçersiz seçim!{Colors.END}")
                input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
                return
            
            operation = available_ops[choice_idx]
            
            # Sayıları al
            num1 = float(input(f"{Colors.BLUE}Birinci sayı:{Colors.END} "))
            num2 = float(input(f"{Colors.BLUE}İkinci sayı:{Colors.END} "))
            
            # İşlemi yap
            if operation == 'toplama':
                correct_result = num1 + num2
                op_symbol = '+'
            elif operation == 'çıkarma':
                correct_result = num1 - num2
                op_symbol = '-'
            elif operation == 'çarpma':
                correct_result = num1 * num2
                op_symbol = '×'
            elif operation == 'bölme':
                if num2 == 0:
                    print(f"{Colors.FAIL}Hata: Sıfıra bölme hatası!{Colors.END}")
                    self.error_count += 1
                    self.score -= 10
                    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
                    return
                correct_result = num1 / num2
                op_symbol = '÷'
            
            # Kullanıcının cevabını al
            user_answer = float(input(f"{Colors.BLUE}Sonuç ({num1} {op_symbol} {num2} = ?):{Colors.END} "))
            
            # Cevabı kontrol et (ondalık toleransı ile)
            if abs(user_answer - correct_result) <= 1e-6:
                print(f"{Colors.GREEN}{Colors.BOLD}✓ Doğru! İşlem başarılı.{Colors.END}")
                self.bonus_points += 1
                self.score += 15
                self.used_operations[operation] = True
                
                # Rastgele bir harf aç
                unopened_indices = [i for i, char in enumerate(self.masked_word) if char == '_']
                if unopened_indices:
                    random_idx = random.choice(unopened_indices)
                    self.masked_word[random_idx] = self.word[random_idx]
                    print(f"{Colors.GREEN}Bonus: '{self.word[random_idx]}' harfi açıldı!{Colors.END}")
            else:
                print(f"{Colors.FAIL}✗ Yanlış! Doğru cevap: {correct_result:.2f}{Colors.END}")
                self.error_count += 1
                self.score -= 10
            
        except ValueError:
            print(f"{Colors.FAIL}Geçersiz giriş! Lütfen sayı girin.{Colors.END}")
        except Exception as e:
            print(f"{Colors.FAIL}Bir hata oluştu: {e}{Colors.END}")
        
        input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
    
    def get_hint(self):
        """İpucu al"""
        if self.hint_used:
            print(f"{Colors.WARNING}İpucunu zaten kullandınız!{Colors.END}")
            return False
        
        if self.bonus_points < 1:
            print(f"{Colors.FAIL}Yetersiz bonus! İpucu için 1 bonus puan gerekli.{Colors.END}")
            return False
        
        self.bonus_points -= 1
        self.hint_used = True
        print(f"{Colors.GREEN}{Colors.BOLD}İpucu: Kategori → {self.category.upper()}{Colors.END}")
        return True
    
    def is_won(self):
        """Oyun kazanıldı mı?"""
        return '_' not in self.masked_word
    
    def is_lost(self):
        """Oyun kaybedildi mi?"""
        return self.error_count >= self.max_errors
    
    def save_score(self, player_name):
        """Skoru kaydet"""
        score_data = {
            'player': player_name,
            'score': self.score,
            'word': self.word,
            'category': self.category,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Mevcut skorları oku
        scores = []
        if os.path.exists('scores.json'):
            try:
                with open('scores.json', 'r', encoding='utf-8') as f:
                    scores = json.load(f)
            except:
                scores = []
        
        # Yeni skoru ekle
        scores.append(score_data)
        
        # Skorları sırala (en yüksek 5)
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:5]
        
        # Kaydet
        with open('scores.json', 'w', encoding='utf-8') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        
        return scores
    
    def display_scores(self, scores):
        """Skorları göster"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'═' * 50}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}EN YÜKSEK 5 SKOR{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'═' * 50}{Colors.END}\n")
        
        for i, score in enumerate(scores, 1):
            print(f"{Colors.CYAN}{i}. {Colors.BOLD}{score['player']}{Colors.END} - "
                  f"{Colors.GREEN}{score['score']} puan{Colors.END} - "
                  f"{Colors.BLUE}{score['word']}{Colors.END} "
                  f"({score['category']}) - {score['date']}")
        
        print(f"\n{Colors.HEADER}{'═' * 50}{Colors.END}")

def main():
    """Ana oyun döngüsü"""
    game = CalcHangGame()
    
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════╗")
    print("║   CALC & HANG — İŞLEM YAP, HARFİ KURTAR      ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    player_name = input(f"{Colors.CYAN}Oyuncu adınızı girin:{Colors.END} ").strip()
    if not player_name:
        player_name = "Oyuncu"
    
    input(f"\n{Colors.GREEN}Oyuna başlamak için Enter'a basın...{Colors.END}")
    
    # Ana oyun döngüsü
    while True:
        game.display_game_state()
        
        # Kazanma/kaybetme kontrolü
        if game.is_won():
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TEBRİKLER! KAZANDINIZ! 🎉{Colors.END}")
            print(f"{Colors.CYAN}Kelime: {Colors.BOLD}{game.word}{Colors.END}")
            game.score += 50  # Kazanma bonusu
            break
        
        if game.is_lost():
            print(f"\n{Colors.FAIL}{Colors.BOLD}💀 KAYBETTİNİZ! 💀{Colors.END}")
            print(f"{Colors.CYAN}Doğru kelime: {Colors.BOLD}{game.word}{Colors.END}")
            game.score -= 20  # Kaybetme cezası
            break
        
        # Menü
        print(f"{Colors.BOLD}Ne yapmak istersiniz?{Colors.END}")
        print(f"  {Colors.GREEN}1.{Colors.END} Harf tahmin et")
        print(f"  {Colors.GREEN}2.{Colors.END} İşlem çöz (bonus kazan)")
        print(f"  {Colors.GREEN}3.{Colors.END} İpucu al (1 bonus)")
        print(f"  {Colors.GREEN}4.{Colors.END} Çıkış (q)")
        
        choice = input(f"\n{Colors.BLUE}Seçiminiz:{Colors.END} ").strip().lower()
        
        if choice == '1':
            letter = input(f"{Colors.BLUE}Harf tahmin edin:{Colors.END} ").strip()
            success, message = game.guess_letter(letter)
            print(f"\n{message}")
            input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
            
        elif choice == '2':
            game.calculate()
            
        elif choice == '3':
            game.get_hint()
            input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
            
        elif choice == '4' or choice == 'q':
            print(f"\n{Colors.WARNING}Oyun sonlandırılıyor...{Colors.END}")
            break
        
        else:
            print(f"{Colors.FAIL}Geçersiz seçim!{Colors.END}")
            input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.END}")
    
    # Oyun sonu
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'═' * 50}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}OYUN SONU - PUAN TABLOSU{Colors.END}")
    print(f"{Colors.HEADER}{'═' * 50}{Colors.END}")
    print(f"{Colors.CYAN}Toplam Skor:{Colors.END} {Colors.BOLD}{game.score}{Colors.END}")
    print(f"{Colors.CYAN}Bonus Puan:{Colors.END} {Colors.BOLD}{game.bonus_points}{Colors.END}")
    print(f"{Colors.CYAN}Hata Sayısı:{Colors.END} {Colors.BOLD}{game.error_count}/{game.max_errors}{Colors.END}")
    print(f"{Colors.HEADER}{'═' * 50}{Colors.END}\n")
    
    # Skoru kaydet ve göster
    scores = game.save_score(player_name)
    game.display_scores(scores)
    
    # Tekrar oyna
    play_again = input(f"\n{Colors.CYAN}Tekrar oynamak ister misiniz? (e/h):{Colors.END} ").strip().lower()
    if play_again == 'e':
        game.reset_game()
        main()
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Oynadığınız için teşekkürler! 👋{Colors.END}\n")

if __name__ == "__main__":
    main()
