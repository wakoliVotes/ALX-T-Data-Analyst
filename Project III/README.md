# Prosper Loan Dataset Exploration
## by Votes W. Wakoli


## Dataset

> Provide basic information about your dataset in this section. If you selected your own dataset, make sure you note the source of your data and summarize any data wrangling steps that you performed before you started your exploration.

ProsperLoadData forms the basis of this exploration, and it comprises information on loans. The structure is 113,937 rows representing loan listings, supple,ented with different variables totaling 81 that gives more information about the loans. Overall, the dataset contains different data types, ranging from categorical, ordinal, nominal and continuous types of data in examining the loans.


## Summary of Findings

> Summarize all of your findings from your exploration here, whether you plan on bringing them into your explanatory presentation or not.

Using the ProsperLoadData, I chose eight (8) main variables as the focus out of all 81 in the dataset. By combining quantative and qualitative variables, it was possible to make a more informed analysis and get better insights of the dataset. The interest variables were:
- "LoanStatus"
- "LoanOriginalAmount"
- "BorrowerRate"
- "Occupation"
- "IncomeRange"
- "EmploymentStatus"
- "EstimatedReturn"
- "EstimatedLoss

Of the eight variables, only six (6) formed part of the explanatory presentation, with core findings as explained below;

First, Of the examined LoanStatus, the majority of borrowers have 'Current' loan status, followed by Completed. And with lower Default proportion ( 5018), which can be seen as good for the financial institution. Secondly, the Original Loan Amount across most borrowers were 4000, 15000, 12407, 100000, 5000 and 2000, despite the data having multiple peaks. Thirdly, interest rate (BorrowerRate) was normally distributed across the loans, with most rates lying between 0.1 to 0.2 range, and peak with most loans at 0.15 rate. Of all borrowers, the top most were  Porfessional, Computer Programmer, Executive, Teacher, Adminstration Assistant, Analyst, Sales - Commission, Accountant/CPA, Clerical, and Sales - Retail, of which the top income ranges were 25,000-49,999 and 50,000-74,999. However, most borrowers were Employed and those in Full-Time professions.
In bivariate analysis, the box plots showed  a relationship between Loan Status and Interest Rates. Also, from box plot's median lines, Charged Off, Defaulted and Past Due loans have the highest BorrowerRate. Current, Completed, Final Payment in Progres and Cancelled have noticeably lesser Rates than the above variables
There are Outliers in the Completed and the Defaulted* loan status, shown by the outside dots in box plots. Lastly, on Loan Status and Original Loan Amount, 
Based on the median points (white dot in the violin), Status of Loan has noticeable association with Loan Original Amount, violin plot's medians showed useful association in the variables. That is, Current has the highest median on Loan Status, followed by Past Due. Completed, Charge off, and Defaulted have average levels in Original Loan Amounts. Since the thick bars in the center represents the interquartile range, most of the points lie on the right. This means most of the distribution is right skewed, as most points are on the right.
Of the 5 variables, LoanOriginalAmount has negative correlation with BorrowerRate (-0.33), EstimatedLoss (-0.43), EstimatedReturn (-0.29). BorrowerRate has positive correlation with EstimatedLoss (0.95), EstimatedReturn (0.82), and negative for LoanOriginalAmount (-0.33).


## Key Insights for Presentation

> Select one or two main threads from your exploration to polish up for your presentation. Note any changes in design from your exploration step here.

- In the exploration, eight (8) variables were examined. However, for presentation (explanatory), the focus is on only six (6) variables. That is;
1. 'LoanStatus',
2. 'LoanOriginalAmount',
3. 'BorrowerRate',
4. 'Occupation',
5. 'IncomeRange',
6. 'EstimatedReturn'

- The reason for choosing only these variables is that for the **target audience**, i.e., **Bank Management**, there is more interest in understanding how  loans are doing, and decipher some main issues impacting the loans. As such, by comparing BorrowerRate and Original Loan Amounts, there will be better planning on what to market more and measures to implement. Also, by examining different Loan Statuses and how different members perform across the levels, it helps infer how management can adopt proper control measures and plan better incase of past due status or defaulted cases. Overall, by using these four (4) variable, there is better planning and management for the **Bank Managers and Financial Institutions** now and in future.