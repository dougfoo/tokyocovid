import React from 'react';
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import {BarChart, Bar, XAxis, Tooltip, Legend} from 'recharts';
import { withTheme } from '@material-ui/styles';

function SimpleReactiveBarChart(props) {
  const { data } = props;
  
  return (
    <ResponsiveContainer height={375}>
      <BarChart data={data}>
        <XAxis dataKey="name"/>
        <Tooltip/>
        <Legend />
        <Bar name="yesterday" dataKey="value" fill="teal" />
        <Bar name="today" dataKey="value2" fill="grey" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default withTheme(SimpleReactiveBarChart);