import React from 'react';
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import {PieChart, Pie,  Cell, Tooltip, Legend} from 'recharts';
import { withTheme } from '@material-ui/styles';

function SimpleReactivePieChart(props) {
  const { data } = props;
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({
    cx, cy, midAngle, innerRadius, outerRadius, percent, index,
  }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
        {`${(percent * 100).toFixed(0)}%`} {(data[index].value2-data[index].value > 0) ? `+` : ` `} {`${(data[index].value2-data[index].value)}`}
      </text>
    );
  };

  return (
    <ResponsiveContainer height={375}>
      <PieChart margin={{ top: 0, left: 0, right: 0, bottom: 0 }}>
        <Pie data={data} labelLine={false} label={renderCustomizedLabel}
          fill="#8884d8" dataKey="value">
          {
            data.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
          }
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default withTheme(SimpleReactivePieChart);