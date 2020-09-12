import React from 'react';
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import {BarChart, Bar, XAxis, Tooltip, Legend} from 'recharts';
import { withTheme } from '@material-ui/styles';

function SimpleReactiveBarChart(props) {
  const { data } = props;
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <ResponsiveContainer height={375}>
      <BarChart data={data}>
        <XAxis dataKey="name"/>
        <Tooltip/>
        <Legend />
        <Bar name="today" dataKey="value" fill="blue" />
        <Bar name="yesterday" dataKey="value2" fill="red" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default withTheme(SimpleReactiveBarChart);