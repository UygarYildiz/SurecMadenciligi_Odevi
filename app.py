from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from process_analyzer import ProcessAnalyzer
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Upload klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global analyzer instance
analyzer = ProcessAnalyzer()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """CSV dosyası yükleme"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'Dosya seçilmedi'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Dosya seçilmedi'})
        
        if file and file.filename.lower().endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Dosyayı analiz et
            success, message = analyzer.load_data(filepath)
            
            if success:
                return jsonify({'success': True, 'message': message})
            else:
                return jsonify({'success': False, 'message': message})
        else:
            return jsonify({'success': False, 'message': 'Lütfen .csv dosyası seçin'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/analyze')
def analyze():
    """Analiz sonuçlarını döndür"""
    try:
        if analyzer.data is None:
            return jsonify({'success': False, 'message': 'Önce bir dosya yükleyin'})
        
        # Tüm analizleri yap
        results = {
            'summary': analyzer.get_summary_stats(),
            'case_durations': analyzer.analyze_case_durations(),
            'activity_frequency': analyzer.analyze_activity_frequency(),
            'transitions': analyzer.analyze_transitions(),
            'charts': {
                'activity_chart': analyzer.create_activity_chart(),
                'duration_chart': analyzer.create_duration_chart(),
                'process_flow': analyzer.create_process_flow()
            }
        }
        
        return jsonify({'success': True, 'data': results})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Analiz hatası: {str(e)}'})

@app.route('/download_sample')
def download_sample():
    """Örnek CSV dosyası oluştur"""
    try:
        import pandas as pd
        from datetime import datetime, timedelta
        import random
        
        # Örnek veri oluştur
        activities = ['Başvuru Alındı', 'Doküman Kontrolü', 'Onay Bekliyor', 'İşlem Tamamlandı', 'Arşivlendi']
        cases = []
        
        for case_id in range(1, 21):  # 20 case
            start_time = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 30))
            
            for i, activity in enumerate(activities):
                activity_start = start_time + timedelta(hours=i*2, minutes=random.randint(0, 60))
                activity_end = activity_start + timedelta(minutes=random.randint(30, 180))
                
                cases.append({
                    'Case ID': f'CASE_{case_id:03d}',
                    'Activity Name': activity,
                    'Start Time': activity_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'End Time': activity_end.strftime('%Y-%m-%d %H:%M:%S')
                })
                
                start_time = activity_end
        
        # DataFrame oluştur ve kaydet
        df = pd.DataFrame(cases)
        sample_path = 'sample_data.csv'
        df.to_csv(sample_path, index=False)
        
        return jsonify({'success': True, 'message': 'Örnek dosya oluşturuldu: sample_data.csv'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Örnek dosya oluşturma hatası: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
