window.onload = async function () {
  const response = await fetch('/api/analysis-data');
  const data = await response.json();

  // Summary text
  document.getElementById("summary").innerHTML =
    `<p><strong>Total Jobs:</strong> ${data.total_jobs}</p>`;

  // Companies Chart
  const companyNames = Object.keys(data.companies);
  const companyCounts = Object.values(data.companies);

  const companyChart = {
    x: companyNames,
    y: companyCounts,
    type: 'bar',
    marker: { color: 'rgb(52, 152, 219)' }
  };

  Plotly.newPlot('companyChart', [companyChart], {
    title: 'Top 10 Hiring Companies',
    xaxis: { title: 'Company' },
    yaxis: { title: 'Job Count' }
  });

  // Locations Chart
  const locationNames = Object.keys(data.locations);
  const locationCounts = Object.values(data.locations);

  const locationChart = {
    labels: locationNames,
    values: locationCounts,
    type: 'pie'
  };

  Plotly.newPlot('locationChart', [locationChart], {
    title: 'Top 10 Job Locations'
  });
};
