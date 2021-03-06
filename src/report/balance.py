import numpy as np
import matplotlib.pyplot as plt
import report.analyzer as analyzer
import pandas as pd


class BalanceSheetAnalyzer(analyzer.Analyzer):
    def __init__(self, file_name):
        analyzer.Analyzer.__init__(self, file_name)
        self.read_data()

        self.asset_df = np.NaN
        self.debt_df = np.NaN
        self.equity_df = np.NaN

    def prepare(self):
        df = self.numberic_df

        self.overall_df = df.loc[['流动资产合计(万元)',
                                  '非流动资产合计(万元)',
                                  '资产总计(万元)',
                                  '流动负债合计(万元)',
                                  '非流动负债合计(万元)',
                                  '负债合计(万元)',
                                  '所有者权益(或股东权益)合计(万元)']]

        # 滤除资产部分的数据
        self.asset_df = df.loc[['货币资金(万元)',
                                '应收票据(万元)',
                                '应收账款(万元)',
                                '预付款项(万元)',
                                '其他应收款(万元)',
                                '存货(万元)',
                                '其他流动资产(万元)',
                                '长期股权投资(万元)',
                                '其他长期投资(万元)',
                                '固定资产(万元)',
                                '在建工程(万元)',
                                '无形资产(万元)',
                                '商誉(万元)',
                                '递延所得税资产(万元)',
                                '其他非流动资产(万元)']]
        # print(self.asset_df)

        # 滤除负债部分的数据
        self.debt_df = df.loc[['负债合计(万元)',
                               '短期借款(万元)',
                               '应付票据(万元)',
                               '应付账款(万元)',
                               '预收账款(万元)',
                               '应付职工薪酬(万元)',
                               '应付利息(万元)',
                               '其他应付款(万元)',
                               '一年内到期的非流动负债(万元)',
                               '其他流动负债(万元)',
                               '长期借款(万元)',
                               '应付债券(万元)',
                               '长期递延收益(万元)',
                               '递延所得税负债(万元)',
                               '其他非流动负债(万元)']]
        # print(self.debt_df)

        # 滤除股东权益部分的数据
        self.equity_df = df['实收资本(或股本)(万元)':'所有者权益(或股东权益)合计(万元)']
        # print(self.equity_df)

    def plot_asset(self):
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.sans-serif'] = ['SimHei']

        # 选择资产部分超过一定百分比的项目，并作图
        asset_rate = self.asset_df[:] / self.numberic_df.loc['资产总计(万元)']
        asset_rate = asset_rate[asset_rate[asset_rate.columns[0]] > 0.05]
        asset_rate = asset_rate.T
        print(asset_rate)

        # 选择负债部分超过一定百分比的项目，并作图
        debt_rate = self.debt_df[:] / self.numberic_df.loc['资产总计(万元)']
        debt_rate = debt_rate[debt_rate[debt_rate.columns[0]] > 0.05]
        debt_rate = debt_rate.T
        print(debt_rate)

        fig, axes = plt.subplots(nrows=2, ncols=1)
        ap = asset_rate.plot(ax=axes[0], figsize=(8,6))
        ap.set_ylabel("百分比")
        ap_vals = ap.get_yticks()
        ap.set_yticklabels(['{:,.2%}'.format(x) for x in ap_vals])

        dp = debt_rate.plot(ax=axes[1], figsize=(8,6))
        dp.set_xlabel("日期")
        dp.set_ylabel("百分比")
        dp_vals = dp.get_yticks()
        dp.set_yticklabels(['{:,.2%}'.format(x) for x in dp_vals])

    def estimate_asset(self):
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.sans-serif'] = ['SimHei']

        # 1.流动资产检查
        current_asset = self.numberic_df.loc[['货币资金(万元)',
                                              '存货(万元)',
                                              '流动资产合计(万元)',
                                              '流动负债合计(万元)']]
        # 2.流动资产价值与账面价值
        current_asset_value = pd.DataFrame(self.numberic_df.loc['实收资本(或股本)(万元)'])
        current_asset_value['每股流动资产价值'] = (self.numberic_df.loc['流动资产合计(万元)'] - self.numberic_df.loc['流动负债合计(万元)']) / self.numberic_df.loc['实收资本(或股本)(万元)']
        book_value = self.numberic_df.loc['归属于母公司股东权益合计(万元)'] - self.numberic_df.loc['无形资产(万元)'] - self.numberic_df.loc['商誉(万元)']
        current_asset_value['每股账面价值'] = book_value / self.numberic_df.loc['实收资本(或股本)(万元)']
        del current_asset_value['实收资本(或股本)(万元)']

        fig, axes = plt.subplots(nrows=2, ncols=1)
        print(current_asset.T)
        cap = current_asset.T.plot(ax=axes[0], figsize=(8,6))
        cap.set_ylabel("数值")
        print(current_asset_value)
        cavp = current_asset_value.plot(ax=axes[1], figsize=(8,6))
        cavp.set_xlabel("日期")
        cavp.set_ylabel("数值")
        plt.show()


    def analyze(self):
        self.prepare()
        self.plot_asset()
        self.estimate_asset()
