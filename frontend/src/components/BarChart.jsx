import { Bar } from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js/auto";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const convertBarChartData = (originalData) => {
  const salaryData = originalData.results;

  if (!salaryData || salaryData.length < 1) return null;

  const labels = salaryData.map((item) => item.City);
  const legend = salaryData[0]["Job Title"];
  const salaries = salaryData.map((item) => item.Salary);

  return {
    labels,
    datasets: [{ label: legend, data: salaries }],
  };
};

function BarChart({ chartData }) {
  if (chartData) return <Bar data={chartData} updateMode="resize" />;
  else return "The datasets are empty!";
}

export default BarChart;
