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
    console.log("This is the Bar Chart Cities", City);
    acc[title].data.push(Salary);
    console.log("This is the acc", acc);
    return acc;
  }, {});

  //console.log("This is the dataset", datasets);

  console.log("This is groupedData", groupedData);

  console.log("This is Object.keys(groupedData)", Object.keys(groupedData));

  for (let key in groupedData) {
    console.log("This is the key", key);
    let labelsArray = groupedData[key].labels;
    for (let i in labelsArray)
    {
    	if (labelsYeet.indexOf(labelsArray[i]) == -1)
    	{
    		labelsYeet.push(labelsArray[i]);
    	}
    }
    // labelsYeet = labelsYeet.concat(groupedData[key].labels);
  }

  console.log("This is labelsYeet", labelsYeet);
    
  const datasets = Object.entries(groupedData).map(([title, data]) => {
    let values = [];
    for (let cityIndex in labelsYeet)
    {
      let city = labelsYeet[cityIndex];
    	let index = data.labels.indexOf(city);
      console.log("City is", city);
      console.log("index is", index);
      console.log("Data labels are", data.labels);
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

  console.log("This is the dataset", datasets);

  return {
    labels: labelsYeet,
    datasets,
  };
};

// export const convertBarChartData = (originalData) => {
//   const salaryData = originalData.results;

//   if (!salaryData || salaryData.length < 1) return null;

//   const labels = salaryData.map((item) => item.City);
//   const legend = salaryData[0]["Job Title"];
//   const salaries = salaryData.map((item) => item.Salary);

//   return {
//     labels,
//     datasets: [{ label: legend, data: salaries }],
//   };
// };

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
