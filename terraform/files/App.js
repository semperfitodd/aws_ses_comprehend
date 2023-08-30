import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, ArcElement, BarElement } from 'chart.js';

Chart.register(CategoryScale, LinearScale, ArcElement, BarElement);

function App() {
  const [data, setData] = useState({ sentimentCounts: {}, topPhrases: {} });

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get('<API_GATEWAY_INVOKE_URL>/comprehend', {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
    const interval = setInterval(fetchData, 300000); // Refresh data every 5 minutes
    return () => clearInterval(interval);
  }, []);

  const sentimentData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        data: [data.sentimentCounts.POSITIVE, data.sentimentCounts.NEGATIVE, data.sentimentCounts.NEUTRAL],
        backgroundColor: ['#4CAF50', '#FF5733', '#FFC300']
      }
    ]
  };

  const options = {
    plugins: {
      legend: {
        display: true,
        position: 'right',
      }
    }
  };

  const dedupePhrases = (phrases) => {
    const seen = new Set();
    return phrases.filter((phrase) => {
      const lowerCasePhrase = phrase.toLowerCase();
      if (seen.has(lowerCasePhrase)) {
        return false;
      }
      seen.add(lowerCasePhrase);
      return Boolean(phrase); // This will also filter out empty strings
    });
  };

return (
    <div className="App">
      <h1>Email Analysis</h1>
      <Bar data={sentimentData} options={options} />
      <table style={{ width: "100%", textAlign: "center" }}>
        <thead>
          <tr>
            <th>Top Positive Phrases</th>
            <th>Top Negative Phrases</th>
            <th>Top Neutral Phrases</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{dedupePhrases(data.topPhrases.POSITIVE || []).join(', ')}</td>
            <td>{dedupePhrases(data.topPhrases.NEGATIVE || []).join(', ')}</td>
            <td>{dedupePhrases(data.topPhrases.NEUTRAL || []).join(', ')}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default App;
