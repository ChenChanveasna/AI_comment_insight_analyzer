document.addEventListener("DOMContentLoaded", () => {
  const payload = window.__ANALYTICS__;

  if (!payload || typeof Chart === "undefined") {
    return;
  }

  const sentimentCanvas = document.getElementById("sentimentChart");
  const wordsCanvas = document.getElementById("wordsChart");

  if (sentimentCanvas) {
    new Chart(sentimentCanvas, {
      type: "doughnut",
      data: {
        labels: payload.labels,
        datasets: [
          {
            data: payload.values,
            backgroundColor: ["#22c55e", "#4dd0e1", "#ef4444"],
            borderColor: "rgba(255, 255, 255, 0.12)",
            borderWidth: 2,
            hoverOffset: 10,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#eef4ff",
              usePointStyle: true,
              padding: 18,
            },
          },
        },
        cutout: "68%",
      },
    });
  }

  if (wordsCanvas) {
    new Chart(wordsCanvas, {
      type: "bar",
      data: {
        labels: payload.topWords.map((entry) => entry.word),
        datasets: [
          {
            label: "Word count",
            data: payload.topWords.map((entry) => entry.count),
            backgroundColor: "rgba(255, 183, 3, 0.8)",
            borderRadius: 12,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              color: "#eef4ff",
            },
            grid: {
              display: false,
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: "#eef4ff",
              precision: 0,
            },
            grid: {
              color: "rgba(255, 255, 255, 0.08)",
            },
          },
        },
      },
    });
  }
});
