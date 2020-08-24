import React, { Component } from "react";
import withStyles from "@material-ui/styles/withStyles";
import { withRouter } from "react-router-dom";
import CssBaseline from "@material-ui/core/CssBaseline";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import Topbar from "./Topbar";
import SimpleReactiveChart from "./SimpleReactiveChart";
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import {
  PieChart, Pie, Sector, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

const backgroundShape = require("../images/shape.svg");

const styles = theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.grey["100"],
    overflow: "hidden",
    background: `url(${backgroundShape}) no-repeat`,
    backgroundSize: "cover",
    backgroundPosition: "0 400px",
    paddingBottom: 200
  },
  grid: {
    width: 1200,
    marginTop: 40,
    [theme.breakpoints.down("sm")]: {
      width: "calc(100% - 20px)"
    }
  },
  paper: {
    padding: theme.spacing(3),
    textAlign: "left",
    color: theme.palette.text.secondary
  },
  rangeLabel: {
    display: "flex",
    justifyContent: "space-between",
    paddingTop: theme.spacing(2)
  },
  topBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 32
  },
  outlinedButtom: {
    textTransform: "uppercase",
    margin: theme.spacing(1)
  },
  actionButtom: {
    textTransform: "uppercase",
    margin: theme.spacing(1),
    width: 152
  },
  blockCenter: {
    padding: theme.spacing(2),
    textAlign: "center"
  },
  block: {
    padding: theme.spacing(2)
  },
  box: {
    marginBottom: 40,
    height: 65
  },
  inlining: {
    display: "inline-block",
    marginRight: 10
  },
  buttonBar: {
    display: "flex"
  },
  alignRight: {
    display: "flex",
    justifyContent: "flex-end"
  },
  noBorder: {
    borderBottomStyle: "hidden"
  },
  loadingState: {
    opacity: 0.05
  },
  loadingMessage: {
    position: "absolute",
    top: "40%",
    left: "40%"
  }
});

class Main extends Component {
  state = {
    learnMoredialog: false,
    getStartedDialog: false,
    dailyData: [],
    dailyDemo: [],
    dailyTrend: []
  };

  openDialog = event => {
    this.setState({ learnMoredialog: true });
  };

  dialogClose = event => {
    this.setState({ learnMoredialog: false });
  };

  openGetStartedDialog = event => {
    this.setState({ getStartedDialog: true });
  };

  closeGetStartedDialog = event => {
    this.setState({ getStartedDialog: false });
  };

  componentDidMount() {
    fetch("data/dailyData.json")
    .then(res => res.json())
    .then(data => {
      console.log(data);
      this.setState({ ...this.state, dailyData: data })
    });
    fetch("data/dailyTrend.json")
    .then(res => res.json())
    .then(data => {
      console.log(data);
      this.setState({ ...this.state, dailyTrend: data })
    });
    fetch("data/dailyDemo.json")
    .then(res => res.json())
    .then(data => {
      console.log(data);
      this.setState({ ...this.state, dailyDemo: data })
    });
  }

  render() {
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
          {`${(percent * 100).toFixed(0)}%`}
        </text>
      );
    };
  
    const { classes } = this.props;
    return (
      <React.Fragment>
        <CssBaseline />
        <Topbar />
        <div className={classes.root}>
          <Grid container justify="center">
            <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                      New Cases Tokyo
                    </Typography>
                    <Typography variant="body2" display="inline">
                     {this.state.dailyData['NewTokyoCase']} &nbsp; 
                    </Typography>
                    <Typography variant="body2" color="error" display="inline">
                    {(this.state.dailyData['TokyoCaseChange'] > 0) ? '+' : '-' } {this.state.dailyData['TokyoCaseChange']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                      7 Day Avg Tokyo
                    </Typography>
                    <Typography variant="body2" gutterBottom display="inline">
                      {this.state.dailyData['TokyoCaseAvg7d']} &nbsp; 
                    </Typography>
                    <Typography variant="body2" color="error" display="inline">
                      {(this.state.dailyData['TokyoCaseChange'] > 0) ? '+' : '-'} {this.state.dailyData['TokyoCaseAvgDiff']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Total Open Tokyo
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                    {this.state.dailyData['TokyoCase']}
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Japan Total Cases
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                     {this.state.dailyData['JapanCase']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Japan Daily New Cases
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      {this.state.dailyData['NewJapanCase']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Death Watch
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      New Deaths: TBA <br/>
                      Total Deaths: TBA <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid container item xs={12}>
                <Grid item xs={12}>
                  <Paper className={classes.paper}>
                    <div>
                      <div className={classes.box}>
                        <Typography color="secondary" gutterBottom>
                          Daily New Case Counts
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          (Tokyo tk, Osaka os)
                        </Typography>
                      </div>
                      <div>
                        <ResponsiveContainer width="99%" height={225}>
                          <LineChart width={600} height={300} data={this.state.dailyTrend}
                            margin={{
                              top: 5, right: 5, left: 5, bottom: 5,
                            }}
                          >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="tok" stroke="#8884d8" activeDot={{ r: 8 }} />
                          </LineChart>                            
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </Paper>
                </Grid>
              </Grid>
              <Grid container item xs={12}>
                <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
                  <Grid item xs={6}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                            Tokyo Daily Breakdown (by Gender)
                          </Typography>
                        </div>
                        <div>
                          <SimpleReactiveChart data={this.state.dailyDemo.slice(0,2)} />
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                  <Grid item xs={6}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                          Tokyo Daily Breakdown (by Age)
                          </Typography>
                        </div>
                        <div>
                          <SimpleReactiveChart data={this.state.dailyDemo.slice(2,12)} />
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
            <Grid container item xs={12}>
              <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
                <Grid item xs={12} md={8}>
                  <Paper className={classes.paper}>
                    <div className={classes.box}>
                      <Typography style={{ textTransform: "uppercase" }} color="secondary" >
                        Photo Library of My Dogs
                      </Typography>
                      <Button onClick={this.openDialog} variant="outlined" className={classes.actionButtom}>
                        To Dogs
                      </Button>
                    </div>
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
          {/* <SwipeDialog
            open={this.state.learnMoredialog}
            onClose={this.dialogClose}
          />
          <InstructionDialog
            open={this.state.getStartedDialog}
            onClose={this.closeGetStartedDialog}
          /> */}
        </div>
      </React.Fragment>
    );
  }
}

export default withRouter(withStyles(styles)(Main));
