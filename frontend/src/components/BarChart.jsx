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
  let labelsYeet = [];

  if (!salaryData || salaryData.length < 1) return null;

  const groupedData = salaryData.reduce((acc, item) => {
    const { City, Salary, "Job Title": title } = item;
    if (!acc[title]) {
      acc[title] = { labels: [], data: [] };
    }
    acc[title].labels.push(City);
    acc[title].data.push(Salary);
    return acc;
  }, {});

  for (let key in groupedData) {
    let labelsArray = groupedData[key].labels;
    for (let i in labelsArray)
    {
    	if (labelsYeet.indexOf(labelsArray[i]) == -1)
    	{
    		labelsYeet.push(labelsArray[i]);
    	}
    }
  }

  const datasets = Object.entries(groupedData).map(([title, data]) => {
    let values = [];
    for (let cityIndex in labelsYeet)
    {
      let city = labelsYeet[cityIndex];
    	let index = data.labels.indexOf(city);
    	if (index > -1)
    	{
    		values.push(data.data[index]);
    	}
    	else
    	{
    		values.push(0);
    	}
    }
    return {
    	label: title,
    	data: values,
    }
  });

  return {
    labels: labelsYeet,
    datasets,
  };
};

function BarChart({ chartData }) {
  if (chartData)
    return (
      <Bar
        data={chartData}
        updateMode="resize"
        options={{ maintainAspectRatio: false }}
      />
    );
  else return "No Results Found";
}

export default BarChart;
