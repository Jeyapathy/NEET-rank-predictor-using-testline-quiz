import type React from "react"

const StudentRankPredictor: React.FC = () => {
  return (
    <div className="bg-gray-100 min-h-screen">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Student Rank Predictor</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Performance Analysis</h2>
            <h3 className="text-lg font-medium mb-2">Topic Performance</h3>
            <ul className="list-disc list-inside mb-4">
              <li>Physics: 75.00%</li>
              <li>Chemistry: 33.00%</li>
              <li>Biology: 67.00%</li>
            </ul>
            <h3 className="text-lg font-medium mb-2">Difficulty Performance</h3>
            <ul className="list-disc list-inside mb-4">
              <li>Easy: 67.00%</li>
              <li>Medium: 50.00%</li>
              <li>Hard: 67.00%</li>
            </ul>
            <p>Average Score: 80.00</p>
            <p>Improvement Trend: 1.75 points per quiz</p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Predictions</h2>
            <p className="text-lg mb-2">
              Predicted NEET Rank: <span className="font-bold">523</span>
            </p>
            <p className="text-lg mb-4">
              Predicted College: <span className="font-bold">Christian Medical College (CMC), Vellore</span>
            </p>
            <div className="mb-4">
              <h3 className="text-lg font-medium mb-2">Topic Performance</h3>
              <img src="/placeholder.svg?height=300&width=500" alt="Topic Performance" className="w-full" />
            </div>
            <div>
              <h3 className="text-lg font-medium mb-2">Historical Score Trend</h3>
              <img src="/placeholder.svg?height=300&width=500" alt="Historical Score Trend" className="w-full" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StudentRankPredictor

