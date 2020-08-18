import React from 'react';
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';
import { withTheme } from '@material-ui/styles';

function SimpleReactiveChart(props) {
  const { data } = props;
  return (
    <ResponsiveContainer width="99%" height={225}>
     <BarChart
        width={500}
        height={300}
        data={data}
        margin={{
          top: 5, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="m" fill="#8884d8" />
        <Bar dataKey="f" fill="#82ca9d" />
        <Bar dataKey="yg" fill="#0804d8" />
        <Bar dataKey="old" fill="#028a9d" />
        <Bar dataKey="tk" fill="#888408" />
        <Bar dataKey="ex" fill="#82ca0d" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default withTheme(SimpleReactiveChart);