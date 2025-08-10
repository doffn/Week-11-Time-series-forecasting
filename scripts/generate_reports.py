#!/usr/bin/env python3
"""
Generate comprehensive portfolio analysis reports
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pickle
import json
from jinja2 import Template
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def load_analysis_results():
    """
    Load all analysis results from pickle files
    """
    results = {}
    
    try:
        with open('data/arima_results.pkl', 'rb') as f:
            results['arima'] = pickle.load(f)
        logger.info("✓ ARIMA results loaded")
    except FileNotFoundError:
        logger.warning("ARIMA results not found")
        results['arima'] = None
    
    try:
        with open('data/lstm_results.pkl', 'rb') as f:
            results['lstm'] = pickle.load(f)
        logger.info("✓ LSTM results loaded")
    except FileNotFoundError:
        logger.warning("LSTM results not found")
        results['lstm'] = None
    
    try:
        with open('data/portfolio_recommendation.pkl', 'rb') as f:
            results['portfolio'] = pickle.load(f)
        logger.info("✓ Portfolio results loaded")
    except FileNotFoundError:
        logger.warning("Portfolio results not found")
        results['portfolio'] = None
    
    try:
        with open('data/risk_management_summary.pkl', 'rb') as f:
            results['risk'] = pickle.load(f)
        logger.info("✓ Risk management results loaded")
    except FileNotFoundError:
        logger.warning("Risk management results not found")
        results['risk'] = None
    
    return results

def generate_executive_summary(results):
    """
    Generate executive summary
    """
    summary = {
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'analysis_period': '2015-07-01 to 2025-07-31',
        'assets_analyzed': ['TSLA', 'BND', 'SPY']
    }
    
    # Model performance
    if results['arima'] and results['lstm']:
        arima_rmse = results['arima']['forecast_accuracy']['rmse']
        lstm_rmse = results['lstm']['forecast_accuracy']['rmse']
        
        summary['best_model'] = 'LSTM' if lstm_rmse &lt; arima_rmse else 'ARIMA'
        summary['best_model_rmse'] = min(arima_rmse, lstm_rmse)
    
    # Portfolio metrics
    if results['portfolio']:
        summary['recommended_allocation'] = results['portfolio']['weights']
        summary['expected_return'] = results['portfolio']['expected_return'] * 100
        summary['expected_volatility'] = results['portfolio']['expected_volatility'] * 100
        summary['sharpe_ratio'] = results['portfolio']['sharpe_ratio']
    
    # Risk metrics
    if results['risk']:
        summary['current_var_95'] = results['risk']['current_risk_metrics']['var_95'] * 100
        summary['risk_status'] = results['risk']['alert_status']
    
    return summary

def create_html_report(results, summary):
    """
    Create comprehensive HTML report
    """
    html_template = """
    &lt;!DOCTYPE html>
    <html>
    <head>
        <title>Portfolio Optimization Analysis Report</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            .header {
                text-align: center;
                border-bottom: 3px solid #2c3e50;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            .header h1 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            .section {
                margin: 30px 0;
                padding: 20px;
                border-left: 4px solid #3498db;
                background-color: #f8f9fa;
            }
            .section h2 {
                color: #2c3e50;
                margin-top: 0;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .metric-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                color: #3498db;
            }
            .metric-label {
                color: #7f8c8d;
                margin-top: 5px;
            }
            .allocation-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            .allocation-table th,
            .allocation-table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            .allocation-table th {
                background-color: #3498db;
                color: white;
            }
            .status-good { color: #27ae60; }
            .status-warning { color: #f39c12; }
            .status-critical { color: #e74c3c; }
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Portfolio Optimization Analysis Report</h1>
                <p>Time Series Forecasting & Modern Portfolio Theory</p>
                <p><strong>Generated:</strong> {{ summary.generation_date }}</p>
                <p><strong>Analysis Period:</strong> {{ summary.analysis_period }}</p>
            </div>

            <div class="section">
                <h2>Executive Summary</h2>
                <p>This report presents a comprehensive analysis of portfolio optimization using advanced time series forecasting models and Modern Portfolio Theory. The analysis covers three key assets: Tesla (TSLA), Vanguard Total Bond Market ETF (BND), and S&P 500 ETF (SPY).</p>
                
                <div class="metrics-grid">
                    {% if summary.best_model %}
                    <div class="metric-card">
                        <div class="metric-value">{{ summary.best_model }}</div>
                        <div class="metric-label">Best Forecasting Model</div>
                    </div>
                    {% endif %}
                    
                    {% if summary.expected_return %}
                    <div class="metric-card">
                        <div class="metric-value">{{ "%.1f"|format(summary.expected_return) }}%</div>
                        <div class="metric-label">Expected Annual Return</div>
                    </div>
                    {% endif %}
                    
                    {% if summary.sharpe_ratio %}
                    <div class="metric-card">
                        <div class="metric-value">{{ "%.3f"|format(summary.sharpe_ratio) }}</div>
                        <div class="metric-label">Sharpe Ratio</div>
                    </div>
                    {% endif %}
                    
                    {% if summary.current_var_95 %}
                    <div class="metric-card">
                        <div class="metric-value">{{ "%.2f"|format(summary.current_var_95) }}%</div>
                        <div class="metric-label">Daily VaR (95%)</div>
                    </div>
                    {% endif %}
                </div>
            </div>

            {% if summary.recommended_allocation %}
            <div class="section">
                <h2>Recommended Portfolio Allocation</h2>
                <table class="allocation-table">
                    <thead>
                        <tr>
                            <th>Asset</th>
                            <th>Allocation</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for asset, weight in summary.recommended_allocation.items() %}
                        <tr>
                            <td><strong>{{ asset }}</strong></td>
                            <td>{{ "%.1f"|format(weight * 100) }}%</td>
                            <td>
                                {% if asset == 'TSLA' %}Tesla Inc. - Growth equity component{% endif %}
                                {% if asset == 'BND' %}Vanguard Total Bond Market ETF - Fixed income component{% endif %}
                                {% if asset == 'SPY' %}SPDR S&P 500 ETF - Broad market exposure{% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}

            <div class="section">
                <h2>Model Performance Summary</h2>
                {% if results.arima and results.lstm %}
                <table class="allocation-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>RMSE</th>
                            <th>MAE</th>
                            <th>Directional Accuracy</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>ARIMA</td>
                            <td>{{ "%.6f"|format(results.arima.forecast_accuracy.rmse) }}</td>
                            <td>{{ "%.6f"|format(results.arima.forecast_accuracy.mae) }}</td>
                            <td>{{ "%.1f"|format(results.arima.forecast_accuracy.directional_accuracy) }}%</td>
                            <td>{% if results.arima.forecast_accuracy.rmse &lt; results.lstm.forecast_accuracy.rmse %}<span class="status-good">Best</span>{% else %}<span class="status-warning">Good</span>{% endif %}</td>
                        </tr>
                        <tr>
                            <td>LSTM</td>
                            <td>{{ "%.6f"|format(results.lstm.forecast_accuracy.rmse) }}</td>
                            <td>{{ "%.6f"|format(results.lstm.forecast_accuracy.mae) }}</td>
                            <td>{{ "%.1f"|format(results.lstm.forecast_accuracy.directional_accuracy) }}%</td>
                            <td>{% if results.lstm.forecast_accuracy.rmse &lt; results.arima.forecast_accuracy.rmse %}<span class="status-good">Best</span>{% else %}<span class="status-warning">Good</span>{% endif %}</td>
                        </tr>
                    </tbody>
                </table>
                {% else %}
                <p>Model performance data not available.</p>
                {% endif %}
            </div>

            {% if results.risk %}
            <div class="section">
                <h2>Risk Management Status</h2>
                <p><strong>Current Risk Level:</strong> 
                    <span class="{% if results.risk.alert_status == 'Normal' %}status-good{% elif results.risk.alert_status == 'Warning' %}status-warning{% else %}status-critical{% endif %}">
                        {{ results.risk.alert_status }}
                    </span>
                </p>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{{ "%.2f"|format(results.risk.current_risk_metrics.var_95 * 100) }}%</div>
                        <div class="metric-label">Daily VaR (95%)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ "%.2f"|format(results.risk.current_risk_metrics.var_99 * 100) }}%</div>
                        <div class="metric-label">Daily VaR (99%)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ "%.2f"|format(results.risk.current_risk_metrics.portfolio_volatility * 100) }}%</div>
                        <div class="metric-label">Annual Volatility</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ results.risk.regime_analysis.current_regime }}</div>
                        <div class="metric-label">Market Regime</div>
                    </div>
                </div>

                <h3>Risk Management Recommendations</h3>
                <ul>
                    {% for recommendation in results.risk.recommendations %}
                    <li>{{ recommendation }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}

            <div class="section">
                <h2>Key Findings & Recommendations</h2>
                <h3>Model Selection</h3>
                <ul>
                    <li>{% if summary.best_model %}{{ summary.best_model }} model selected based on superior forecasting accuracy{% else %}Model comparison data not available{% endif %}</li>
                    <li>Regular model retraining recommended to maintain performance</li>
                    <li>Ensemble methods may provide additional robustness</li>
                </ul>

                <h3>Portfolio Construction</h3>
                <ul>
                    <li>Optimal allocation balances growth potential with risk management</li>
                    <li>Diversification across asset classes reduces portfolio volatility</li>
                    <li>Monthly rebalancing recommended to maintain target allocation</li>
                </ul>

                <h3>Risk Management</h3>
                <ul>
                    <li>Implement dynamic position sizing based on market volatility</li>
                    <li>Regular stress testing to assess portfolio resilience</li>
                    <li>Monitor regime changes for tactical allocation adjustments</li>
                </ul>
            </div>

            <div class="section">
                <h2>Implementation Guidelines</h2>
                <h3>Immediate Actions</h3>
                <ul>
                    <li>Implement recommended portfolio allocation</li>
                    <li>Set up automated rebalancing system</li>
                    <li>Establish risk monitoring dashboard</li>
                </ul>

                <h3>Ongoing Monitoring</h3>
                <ul>
                    <li>Daily: Risk metrics and portfolio performance</li>
                    <li>Weekly: Model performance and market regime analysis</li>
                    <li>Monthly: Portfolio rebalancing and stress testing</li>
                    <li>Quarterly: Model retraining and strategy review</li>
                </ul>

                <h3>Risk Controls</h3>
                <ul>
                    <li>Maximum daily loss limit: 3% of portfolio value</li>
                    <li>Position size limits: No single asset > 50% allocation</li>
                    <li>Volatility threshold: Reduce positions if portfolio vol > 25%</li>
                </ul>
            </div>

            <div class="footer">
                <p><strong>Disclaimer:</strong> This analysis is for educational and research purposes only. Past performance does not guarantee future results. Please consult with qualified financial professionals before making investment decisions.</p>
                <p>Report generated by Portfolio Optimization System v1.0</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_content = template.render(results=results, summary=summary)
    
    return html_content

def save_json_summary(results, summary):
    """
    Save analysis summary as JSON
    """
    json_summary = {
        'metadata': {
            'generation_date': summary['generation_date'],
            'analysis_period': summary['analysis_period'],
            'assets_analyzed': summary['assets_analyzed']
        },
        'model_performance': {},
        'portfolio_metrics': {},
        'risk_metrics': {}
    }
    
    # Model performance
    if results['arima']:
        json_summary['model_performance']['arima'] = results['arima']['forecast_accuracy']
    
    if results['lstm']:
        json_summary['model_performance']['lstm'] = results['lstm']['forecast_accuracy']
    
    # Portfolio metrics
    if results['portfolio']:
        json_summary['portfolio_metrics'] = {
            'weights': results['portfolio']['weights'],
            'expected_return': results['portfolio']['expected_return'],
            'expected_volatility': results['portfolio']['expected_volatility'],
            'sharpe_ratio': results['portfolio']['sharpe_ratio']
        }
    
    # Risk metrics
    if results['risk']:
        json_summary['risk_metrics'] = results['risk']['current_risk_metrics']
        json_summary['risk_metrics']['alert_status'] = results['risk']['alert_status']
    
    return json_summary

def main():
    """
    Main report generation function
    """
    logger.info("Starting report generation...")
    
    try:
        # Load analysis results
        results = load_analysis_results()
        
        # Generate executive summary
        summary = generate_executive_summary(results)
        
        # Create reports directory
        os.makedirs('reports', exist_ok=True)
        
        # Generate HTML report
        html_content = create_html_report(results, summary)
        html_path = f"reports/portfolio_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ HTML report saved to {html_path}")
        
        # Generate JSON summary
        json_summary = save_json_summary(results, summary)
        json_path = f"reports/portfolio_analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(json_path, 'w') as f:
            json.dump(json_summary, f, indent=2, default=str)
        
        logger.info(f"✅ JSON summary saved to {json_path}")
        
        # Generate quick stats
        print("\n" + "="*60)
        print("PORTFOLIO ANALYSIS REPORT GENERATED")
        print("="*60)
        print(f"📊 HTML Report: {html_path}")
        print(f"📋 JSON Summary: {json_path}")
        
        if summary.get('best_model'):
            print(f"🏆 Best Model: {summary['best_model']}")
        
        if summary.get('expected_return'):
            print(f"📈 Expected Return: {summary['expected_return']:.1f}%")
        
        if summary.get('sharpe_ratio'):
            print(f"⚖️  Sharpe Ratio: {summary['sharpe_ratio']:.3f}")
        
        print("="*60)
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
