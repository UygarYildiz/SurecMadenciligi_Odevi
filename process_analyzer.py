import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import base64
from collections import Counter, defaultdict

class ProcessAnalyzer:
    def __init__(self):
        self.data = None
        self.processed_data = None
        
    def load_data(self, file_path):
        """CSV dosyasını yükle ve temel doğrulamaları yap"""
        try:
            self.data = pd.read_csv(file_path)
            
            # Gerekli sütunları kontrol et
            required_columns = ['Case ID', 'Activity Name', 'Start Time', 'End Time']
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            
            if missing_columns:
                raise ValueError(f"Eksik sütunlar: {missing_columns}")
            
            # Tarih sütunlarını datetime'a çevir
            self.data['Start Time'] = pd.to_datetime(self.data['Start Time'])
            self.data['End Time'] = pd.to_datetime(self.data['End Time'])
            
            # Süreyi hesapla (dakika cinsinden)
            self.data['Duration'] = (self.data['End Time'] - self.data['Start Time']).dt.total_seconds() / 60
            
            return True, "Veri başarıyla yüklendi!"
            
        except Exception as e:
            return False, f"Veri yükleme hatası: {str(e)}"
    
    def analyze_case_durations(self):
        """Her Case ID'nin toplam süresini hesapla"""
        if self.data is None:
            return None
            
        case_durations = self.data.groupby('Case ID')['Duration'].sum().reset_index()
        case_durations.columns = ['Case ID', 'Total Duration (minutes)']
        
        return {
            'data': case_durations.to_dict('records'),
            'avg_duration': case_durations['Total Duration (minutes)'].mean(),
            'min_duration': case_durations['Total Duration (minutes)'].min(),
            'max_duration': case_durations['Total Duration (minutes)'].max()
        }
    
    def analyze_activity_frequency(self):
        """Aktivite frekanslarını analiz et"""
        if self.data is None:
            return None
            
        activity_counts = self.data['Activity Name'].value_counts()
        
        return {
            'data': activity_counts.to_dict(),
            'most_frequent': activity_counts.index[0],
            'least_frequent': activity_counts.index[-1]
        }
    
    def analyze_transitions(self):
        """Aktiviteler arası geçişleri analiz et"""
        if self.data is None:
            return None
            
        transitions = defaultdict(int)
        
        # Her case için aktivite sırasını bul
        for case_id in self.data['Case ID'].unique():
            case_data = self.data[self.data['Case ID'] == case_id].sort_values('Start Time')
            activities = case_data['Activity Name'].tolist()
            
            # Ardışık aktiviteler arası geçişleri say
            for i in range(len(activities) - 1):
                transition = f"{activities[i]} → {activities[i+1]}"
                transitions[transition] += 1
        
        # En sık geçişleri sırala
        sorted_transitions = dict(sorted(transitions.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'data': sorted_transitions,
            'most_common': list(sorted_transitions.keys())[0] if sorted_transitions else None
        }
    
    def create_activity_chart(self):
        """Aktivite frekans grafiği oluştur"""
        if self.data is None:
            return None

        activity_counts = self.data['Activity Name'].value_counts()

        plt.figure(figsize=(10, 6))
        plt.barh(activity_counts.index, activity_counts.values)
        plt.title('Aktivite Frekansları')
        plt.xlabel('Frekans')
        plt.ylabel('Aktivite')
        plt.tight_layout()

        # Convert to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return f'<img src="data:image/png;base64,{plot_url}" class="img-fluid">'
    
    def create_duration_chart(self):
        """Süre dağılım grafiği oluştur"""
        if self.data is None:
            return None
            
        case_durations = self.data.groupby('Case ID')['Duration'].sum()
        
        fig = px.histogram(
            x=case_durations.values,
            title='Case Süre Dağılımı',
            labels={'x': 'Toplam Süre (dakika)', 'y': 'Case Sayısı'},
            nbins=20
        )
        fig.update_layout(height=400)
        
        return fig.to_html(include_plotlyjs=True, div_id="duration-chart")
    
    def create_process_flow(self):
        """Basit HTML/CSS tabanlı süreç akış diyagramı oluştur"""
        if self.data is None:
            return None

        # Aktivite geçişlerini al
        transitions = self.analyze_transitions()['data']

        if not transitions:
            return '<div class="alert alert-warning">Süreç akış diyagramı için yeterli veri yok.</div>'

        # Benzersiz aktiviteleri bul ve sırala
        activities = list(self.data['Activity Name'].unique())
        activity_counts = self.data['Activity Name'].value_counts().to_dict()

        # En sık geçişleri al (ilk 10)
        top_transitions = dict(list(transitions.items())[:10])
        max_count = max(transitions.values()) if transitions else 1

        # HTML diyagram oluştur
        html = '''
        <div class="process-flow-container" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            color: white;
            font-family: Arial, sans-serif;
            min-height: 400px;
        ">
            <h4 style="text-align: center; margin-bottom: 20px; color: white;">
                🔄 Süreç Akış Diyagramı
            </h4>

            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-bottom: 20px;">
        '''

        # Aktivite kartları
        activity_order = [
            'Başvuru Alındı', 'Başvuru Değerlendirme', 'Belge Kontrolü',
            'Eksik Belge Talebi', 'Belge Tamamlama', 'Müdür Onayı',
            'Üst Yönetici Onayı', 'Hızlı Onay', 'Başvuru Reddi',
            'Ödeme İşlemi', 'Dosya Arşivleme'
        ]

        # Aktiviteleri sırala
        sorted_activities = []
        for activity in activity_order:
            if activity in activities:
                sorted_activities.append(activity)

        # Sıralanmamış aktiviteleri ekle
        for activity in activities:
            if activity not in sorted_activities:
                sorted_activities.append(activity)

        for i, activity in enumerate(sorted_activities):
            count = activity_counts.get(activity, 0)

            # Renk belirleme
            if 'Başvuru' in activity:
                color = '#3498DB'
                icon = '📝'
            elif 'Belge' in activity:
                color = '#F39C12'
                icon = '📄'
            elif 'Onay' in activity:
                color = '#27AE60'
                icon = '✅'
            elif 'Ödeme' in activity:
                color = '#9B59B6'
                icon = '💳'
            elif 'Arşiv' in activity:
                color = '#34495E'
                icon = '📁'
            elif 'Red' in activity:
                color = '#E74C3C'
                icon = '❌'
            else:
                color = '#95A5A6'
                icon = '⚙️'

            # Kısa isim
            short_name = activity.replace('Başvuru ', '').replace('Belge ', '').replace('Dosya ', '')
            if len(short_name) > 12:
                short_name = short_name[:10] + '..'

            html += f'''
                <div style="
                    background: {color};
                    border-radius: 10px;
                    padding: 15px;
                    text-align: center;
                    min-width: 120px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    transition: transform 0.2s;
                    position: relative;
                " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
                    <div style="font-weight: bold; font-size: 12px; margin-bottom: 5px;">{short_name}</div>
                    <div style="font-size: 11px; opacity: 0.9;">Frekans: {count}</div>
                </div>
            '''

            # Ok ekle (son aktivite hariç)
            if i < len(sorted_activities) - 1:
                html += '''
                    <div style="
                        display: flex;
                        align-items: center;
                        color: white;
                        font-size: 20px;
                        margin: 0 5px;
                    ">→</div>
                '''

        html += '''
            </div>

            <div style="margin-top: 20px;">
                <h5 style="color: white; margin-bottom: 15px;">🔥 En Sık Geçişler</h5>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px;">
        '''

        # En sık geçişleri göster
        for i, (transition, count) in enumerate(list(top_transitions.items())[:6]):
            # Geçiş yoğunluğuna göre renk
            intensity = count / max_count
            if intensity >= 0.7:
                bg_color = 'rgba(231, 76, 60, 0.8)'  # Kırmızı
                icon = '🔥'
            elif intensity >= 0.4:
                bg_color = 'rgba(52, 152, 219, 0.8)'  # Mavi
                icon = '⚡'
            else:
                bg_color = 'rgba(149, 165, 166, 0.8)'  # Gri
                icon = '📊'

            html += f'''
                <div style="
                    background: {bg_color};
                    border-radius: 8px;
                    padding: 12px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                ">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 14px; font-weight: 500;">
                            {icon} {transition}
                        </span>
                        <span style="
                            background: rgba(255,255,255,0.3);
                            padding: 4px 8px;
                            border-radius: 12px;
                            font-size: 12px;
                            font-weight: bold;
                        ">{count}</span>
                    </div>
                </div>
            '''

        html += '''
                </div>
            </div>

            <div style="text-align: center; margin-top: 20px; font-size: 12px; opacity: 0.8;">
                💡 Bu diyagram en sık kullanılan süreç yollarını göstermektedir
            </div>
        </div>
        '''

        return html
    
    def get_summary_stats(self):
        """Özet istatistikleri döndür"""
        if self.data is None:
            return None
            
        return {
            'total_cases': self.data['Case ID'].nunique(),
            'total_activities': len(self.data),
            'unique_activities': self.data['Activity Name'].nunique(),
            'date_range': {
                'start': self.data['Start Time'].min().strftime('%Y-%m-%d %H:%M'),
                'end': self.data['End Time'].max().strftime('%Y-%m-%d %H:%M')
            }
        }
