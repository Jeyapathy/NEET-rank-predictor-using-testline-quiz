from flask import Flask, render_template
from analyze_and_predict import analyze_performance, predict_rank, predict_college, generate_visualizations

app = Flask(__name__)

@app.route('/')
def index():
    user_id = 12345  # Example user ID
    performance = analyze_performance(user_id)
    predicted_rank = predict_rank(user_id)
    predicted_college = predict_college(predicted_rank)
    generate_visualizations(user_id)
    
    return render_template('index.html', 
                           performance=performance, 
                           predicted_rank=predicted_rank, 
                           predicted_college=predicted_college)

if __name__ == '__main__':
    app.run(debug=True)

