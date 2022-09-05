#!/usr/bin/env python
# coding: utf-8

# # <center>Part I - Prosper Loan Dataset Exploration</center>
# ![image.png](attachment:image.png)
# ## <center> by Votes W. Wakoli</center>
# 
# ## Table of Contents
# 
# 1. [Introduction](#intro)
# 2. [Preliminary Wrangling](#pre)
# 3. [The structure of the dataset?](#structure)
# 4. [The main feature(s) of interest in your dataset](#features)
# 5. [Features in the dataset in supporting investigation into interest feature(s)](#interest)
# 6. [Univariate Exploration](#uni)
# 7. [Bivariate Exploration](#biv)
# 8. [Univariate Exploration](#mul)
# 9. [Conclusions](#conc)
# 10. [References](#ref)
# 
# 
# ## Introduction
# <div id='intro' />
# > The ProsperLoadData was chosen as the basis in completing this Project III. The dataset comprises information on loans, i.e., 113,937 with different variables totaling 81. Based on the information, one can thus make summaries about the loans documented including original loan amounts, Percent Funded, Estimated Loss, Estimated Return, bowrrower rate and income. In completing the analysis, multiple python libraries are used with the adoption of seaborn as the main visualization package.
# 
# 
# ## Preliminary Wrangling
# <div id='pre' />
# 

# In[4]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import requests
import io

get_ipython().run_line_magic('matplotlib', 'inline')

# suppress warnings from final output
import warnings
warnings.simplefilter("ignore")


# > Load in your dataset and describe its properties through the questions below. Try and motivate your exploration goals through this section.
# 

# In[5]:


# Based on Project II lessons, "request" library can be used to access and save the dataset as below
url = 'https://s3.amazonaws.com/udacity-hosted-downloads/ud651/prosperLoanData.csv'
response = requests.get(url).content
df = pd.read_csv(io.StringIO(response.decode('utf-8')))


# In[6]:


# Saving to csv file and reading the data
df.to_csv('prosperLoansDataset.csv')
df.head()


# > - To answer below questions, doing preliminary assessment of the data is done
# > - First, making a copy of the dataset for use

# In[7]:


loan_data = df.copy()


# In[8]:


# Using desribe to get descriptive statistics
loan_data.describe()


# In[9]:


# Using .shape to check rows and columns
loan_data.shape


# In[10]:


# Uisng .info() method for better insights on the dataset's variables
loan_data.info()


# In[11]:


# Summarizing all columns in the dataset
loan_data.columns


# In[12]:


# Checking totals of each data type in the loan_data
loan_data.dtypes.value_counts()


# ### What is the structure of your dataset?
# <div id='structure' />
# 
# > The ProsperLoanData contains 113,937 rows, i.e., loan information and 81 columns, i.e., specific variables representing additional loan information. Some of the variables in the dataset includes 'ListingKey', 'ListingNumber', 'ListingCreationDate', 'CreditGrade', among others. Based on .info() method, the loan dataset comprises different data types, i.e., float64 (50), int64 (11), object (17) and bool (3)
# 
# ### What is/are the main feature(s) of interest in your dataset?
# <div id='features' />
# 
# > I am interested in finding out contrbuting factors to getting loans. From the dataset, there are 113937 investors, i.e., rows of loans, and this are divided based on 81 variables. With this huge variable scope, it becomes useful to summarize the information and conclude which variables among the 81 have the most impact, have medium impact and those with least impact.
# 
# > One specific focus area is checking if Occupation varies across Borrower Rate, Original Loan Amount or EstmatedLoss and EstimatedReturn. Also, examining how 'IncomeRange' is associated with Loan Status, which contains 'Completed', "Defaulted" status and other elements like 'Cancelled'. Lastly, "LoanOriginalAmount" for the investors is of interest. This is core for planning purposes, especially for the financial institutions or banks providing loans to investors/clients.
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# 
# 
# > The core features in the dataset are the main items in the columns. From the dataset, the focus will be on: 1. "LoanStatus"
# > 2. "LoanOriginalAmount", > 3. "BorrowerRate", > 4. "Occupation", > 5. "IncomeRange", > 6. "EmploymentStatus", > 7. "EstimatedReturn", > 8. "EstimatedLoss"

# ## Univariate Exploration
# 
# <span id='univa'></span>
# 
# > In this section, investigate distributions of individual variables. If
# you see unusual points or outliers, take a deeper look to clean things up
# and prepare yourself to look at relationships between variables.
# 
# > Of all the 81 variables in the ProsperLoanData, the focus for this project are: 1. "LoanStatus" 2. "LoanOriginalAmount" 3. "BorrowerRate" 4. "Occupation" 5. "IncomeRange" 6. "EmploymentStatus" 7. "EstimatedReturn" and 8. EstimatedLoss"

# In[13]:


# Isolating the selected variables only
focus_data = loan_data[['LoanStatus', 'LoanOriginalAmount', 'BorrowerRate', 'Occupation',
                      'IncomeRange', 'EmploymentStatus', 'EstimatedReturn', 'EstimatedLoss']]


# In[14]:


# Overview of chosen variables
focus_data.sample(5)


# ### Loan Status

# ### Question

# > - How is the distribution in loan status across the different loan listings or borrowers?

# #### Visualization

# In[15]:


# Counts per each status for loans
focus_data.LoanStatus.value_counts()


# In[16]:


# Visualization
plt.figure(figsize = [10, 8])
sb.countplot(data = focus_data, x = 'LoanStatus', order = focus_data['LoanStatus'].value_counts().index )
plt.xlabel("Loan Status Across Borrowers")
plt.ylabel("Number of Different Loan Status")
plt.title("Distribution of Loan Status Across Borrowers")
plt.xticks(rotation = 60);


# ##### Making Some Tidiness Tasks

# > - Rewriting "FinalPaymentInProgress" to "Final Payment in Progress" and "Chargedoff" to "Charged Off"

# In[17]:


focus_data['LoanStatus'] = focus_data['LoanStatus'].replace('FinalPaymentInProgress', 'Final Payment In Progress')


# In[18]:


focus_data['LoanStatus'] = focus_data['LoanStatus'].replace('Chargedoff', 'Charged Off')


# - Combining All Past Due Values into One Column since they are all small in proportion

# In[19]:


focus_data['LoanStatus'] = focus_data['LoanStatus'].replace(['Past Due (1-15 days)', 'Past Due (31-60 days)','Past Due (61-90 days)','Past Due (91-120 days)','Past Due (16-30 days)','Past Due (>120 days)'],'Past Due Loans')


# > - Re visualizing the Loan Statuses after making changes

# In[20]:


plt.figure(figsize = [12, 8])
sb.countplot(data = focus_data, x = 'LoanStatus', order = focus_data['LoanStatus'].value_counts().index )
plt.xlabel("Loan Status Across Borrowers")
plt.ylabel("Number of Different Loan Status")
plt.title("Distribution of Loan Status Across Borrowers")
plt.xticks(rotation = 60);


# #### Observations

# > - Of the examined LoanStatus, the majority of borrowers have 'Current' loan status (Current 56576), followed by Completed (38074) and then Charged off (11992)based on how tall the bars are in figure above. From the graph, there is also a noticeable proportional number of borrowers whose loans are Past Due
# > - For the collected data, there is a lower Default proportion ( 5018), which can be seen as good for the financial institution

# ### LoanOriginalAmount

# #### Question: 

# > 1. What is the Distribution of Loan Original Amount Among Borrowers?
# > 2. What are the highest and most common loan amounts accessed by the members?

# #### Visualization

# In[21]:


focus_data.LoanOriginalAmount.value_counts()


# In[22]:


# LoanOriginalAmount is continuous data, and we can use histogram in representing the data
plt.figure(figsize = [10, 8])
sb.histplot(data = focus_data, x = 'LoanOriginalAmount', color = 'blue', kde = True)
plt.xlabel('Counts of Loans')
plt.ylabel('Loan Original Amount')
plt.show()


# #### Observation

# - The histogram shows **multiple peaks**, indicating no clear **normal distribution**
# - Loan Original amount among borrowers is right-skewed, with most of the borrowers lying on the right
# - However, there is no clear bell-shape in the dataset, indicating no normal distribution
# - From the data, the most original amounts are 4000, 15000, 12407, 100000, 5000 and 2000.
# - Based on the histogram, there are **multiple peaks** in the dataset

# ### BorrowerRate

# #### Question

# > 1. How is the distribution of BorrowerRate in the Loan Data?
# > 2. What is the most utilized BorrowerRate across all loans in the ProsperLoanData?

# #### Visualization

# In[23]:


# BorrowerRate is also continuous data, and we can use histogram in representing the data
# plot size
plt.figure(figsize = [12, 10])
# visualization
sb.histplot(data = focus_data, x = 'BorrowerRate', color = 'blue', kde = True)
plt.xlabel('Member Borrower Rate - Interest Rate')
plt.ylabel('Number of Loans per Borrower Rate')
plt.title('Histogram of Borrower Rate For Different Persons')


# #### Observations

# - The BorrowerRate is Skewed to the right
# - Overall, 0.15 as the largest rate, with most of the loans with highest counts had a BorrowerRate of between 0.1 to 0.2
# - There is an evident **Outlier** in the dataset indicated by the highest rising bar in the histogram at around **0.35**
# -  This is an outlier, as it highly differs from other BorrowerRates in the dataset, which seem to lie closer to each other
# - The **least** proportions of loans fell in the range **0.4** to **0.5** as shown above

# ###  "Occupation"

# #### Question

# > - What are the top ten (10) and botton three (3) Occupations mostly using the loan facilities in the Prosper Loan Data?

# #### Visualization

# In[24]:


# Occupation is categorical and hence we can use bar chart
plt.figure(figsize = [20, 20])
sb.countplot(data = focus_data, y = 'Occupation', order = focus_data['Occupation'].value_counts().index )
plt.xlabel("Occupation Status Across Investors")
plt.title("Distribution of Occupation Status Across Borrowers")


# #### Observations

# - Apart from Other, which gives no clear Occupation type, the 10 most professionals in descending order are Porfessional, Computer Programmer, Executive, Teacher, Adminstration Assistant, Analyst, Sales - Commission, Accountant/CPA, Clerical, and Sales - Retail
# - Moreover, of these ten occupations, the Professional group has a massive proportion compared to the next group of Computer Programmer
# - Of all occupations, Judge and Student - Community College and Technical School are the least groups accessing Prosper Loans

# ### IncomeRange

# #### Question

# > - Which are the two (2) most Income Ranges Engaged in Accessing the Prosper Loans and how is the data distributed?

# #### Visualization

# In[25]:


# Income Range is categorical and hence we can use bar chart
plt.figure(figsize = [12, 6])
sb.countplot(data = focus_data, x = 'IncomeRange', order = focus_data['IncomeRange'].value_counts().index )
plt.xlabel("Income Ranges Across Members")
plt.ylabel("Investor Numbers per Income Range")
plt.title("Distribution of Income Range Status Across Investors")
plt.xticks(rotation = 45);


# #### Observation

# - Most borrowers are in 25,000-49,999 totalling 32,192 members. However, this proportion is not too far from second group
# - The second group lie in the 50,000-74,999 with 31050 and in third place 100,000+ with 17337

# ### EmploymentStatus

# #### Question

# > - Who are the most group using the Prosper Loan facility based on Employment Status?

# In[26]:


# EmploymentStatus is categorical and hence we can use bar chart
plt.figure(figsize = [12, 8])
sb.countplot(data = focus_data, x = 'EmploymentStatus', order = focus_data['EmploymentStatus'].value_counts().index )
plt.xlabel("Employment Status Across Investors")
plt.ylabel("Investor Numbers per Employment Status")
plt.title("Distribution of Employment Status Across Investors")
plt.xticks(rotation = 45);


# #### Observations

# - Most users are Employed, and this proportion is so big from the next group of Full time
# - The proportion of Employed using the loans is more than 50% the next group of Full-Time
# - Similarly, the other groups after Full-Time are in smaller proportion, numbers less then 50% of the Full-Time proportion
# - Retired and Not Employed are the least groups utilizing the Prosper Loans

# ### EstimatedLoss

# #### Question

# > - How are the Estimated Loss for the loans distributed among the borrowers?

# #### Visualization

# In[27]:


# EstimatedLoss is continuous data, and we can use histogram in representing the data
plt.figure(figsize = [12, 8])
sb.histplot(data = focus_data, x = 'EstimatedLoss', color ='green', kde = True)
plt.xlabel('Loans Estimated Loss')
plt.ylabel('Number of Estimated Losses for Loans')
plt.title('Counts of Estimated Loss Across Different Loans')


# #### Observations

# - The distribution is slightly normally distributed, and seem like it is right skewed
# - Most of the EstimatedLoss values fall on the right of the histogram's peak
# - Most of EstimatedLoss lies between 0.05 to 0.10, with the least between 0.25 to 0.35 at the histogram's right side

# ### Discuss the distribution(s) of your variable(s) of interest. Were there any unusual points? Did you need to perform any transformations?
# 
# > Completed in Observations
# 
# ### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?
# 
# - Tidying of data was done on these sections:
# 1. On Loan Status, 
#     i. The 'FinalPaymentInProgress' was changed to 'Final Payment In Progress' for better readability
#     ii. Also, on Loan Status 'Chargedoff' was changed to 'Charged off' for better readability
# 2. On Loan Status, upon plotting the first bar graphs, Past Due items were combined into one variable for better visualization

# ## Bivariate Exploration
# <span id="biv"></span>
# 
# > In this section, investigate relationships between pairs of variables in your
# data. Make sure the variables that you cover here have been introduced in some
# fashion in the previous section (univariate exploration).

# ### Occupations and Income Range

# #### Question

# > - How does Income Range of members relate across their occupations in using ProsperLoans?

# #### Visualizations

# In[28]:


# Plotting IncomeRange and Occupation to group the variables for better insights
plt.figure(figsize = [20, 30])
sb.histplot(data = focus_data, y = 'Occupation', hue= 'IncomeRange')
plt.xlabel("Occupation of Borrowers")
plt.title("Distribution of Income Range Against Varied Occupations")


# #### Observations

# > - By comparing Occupation and Income Range, the most noticeable aspect is that among Other group, the most Income Range is 75000 - 99,000
# > - The next noticeable most value is in Executive for which most members earn 100,000+ income as the most recognizable

# ### Employment Status and Loan Status

# #### Question

# > In EmploymentStatus vs Loan Status, which groupings have the most impact across the member's loans?

# #### Visualization

# In[29]:


plt.figure(figsize = [15, 8])
sb.countplot(data = focus_data, x = 'LoanStatus', hue= 'EmploymentStatus', order = focus_data['LoanStatus'].value_counts().index)
plt.xlabel('LoanStatus')
plt.legend(loc = 1, ncol = 8, title = 'Employment Status')
plt.ylabel('Loan Status Counts per Employee Status')
plt.title('Comparison of Loan Status Across Different Employment Status')


# #### Observations

# > - The most impactful grouping in the dataset is the current, which has the bar with the highest peak for Employed
# > - The Employed group has the most current loan status, with other groupings in the same category with very minute levels
# > - In the Completed status, those with Full-time have the highest bar, thus making the most contribution in this group
# > - The same impact is seen in Charged Off, and Defaulted who also have the highest level among the Full-Time members.

# ### Loan Status and Original Loan Amount

# In[30]:


# Here, using violin plots in displaying the distribution across the variables
# defining the plot sizes
plt.figure(figsize = [25, 15])
plt.subplot(2, 2, 2)
sb.violinplot(data = focus_data, x = 'LoanStatus', y = 'LoanOriginalAmount', order = focus_data['LoanStatus'].value_counts().index)
plt.xticks(rotation=45)
plt.xlabel('Status of the Loan')
plt.ylabel('Loan Original Amounts Given');


# - The different Past Dues were combined into one single column in data wrangling for better clarity

# #### Observation

# > - Based on the median points (white dot in the violin), Status of Loan has noticeable association with Loan Original Amount
# > - From the medians, Current has the highest median on Loan Status, followed by Past Due
# > - Completed, Charge off, and Defaulted have average levels in Original Loan Amounts
# > - Since the thick bars in the center represents the interquartile range, most of the points lie on the right
# > - This means most of the distribution is right skewed, as most points are on the right

# ### Loan Status and BorrowRate

# #### Question

# > - Is there is relationship between Loan Status and BorrowerRate>

# In[31]:


# Using boxplot in plotting BorrowerRate vs. Loan Status for subsequent explanations
plt.figure(figsize = [25, 18])

plt.subplot(2, 2, 1)
sb.boxplot(data = focus_data, x = 'LoanStatus', y = 'BorrowerRate', order = focus_data['LoanStatus'].value_counts().index)
plt.xticks(rotation=45)
plt.xlabel('Status of the Loan')
plt.ylabel('Interest Rate')


# #### Observation

# - From the box plots, one can see a relationship between Loan Status and Interest Rates
# - Based on median line on the box plots, Charged Off, Defaulted and Past Due loans have the highest BorrowerRate
# - Current, Completed, Final Payment in Progres and Cancelled have noticeably lesser Rates than the above variables
# - There are **Outliers** in the **Completed** and the **Defaulted*** loan status, shown by the outside dots in **box plots**

# ### LoanOriginalAmount and BorrowRate

# #### Question

# - Is there a positive or negative relationship between LoanOriginalAmount and BorrowRate?

# #### Visualization

# In[33]:


sb.regplot(data = focus_data, x = 'LoanOriginalAmount', y = 'BorrowerRate');
plt.xlabel('Loan Original Amount')
plt.ylabel('Borrow Rate - Interest Rate')


# #### Observation

# > The scatter plot has very high density, with points very close together
# > By looking at the regression line created, it shows negative correlation between LoanOriginalAmount and BorrowRate
# > Hence, as the BorrowerRate - Interest Rate increases, the amount of LoanOriginalAmount decreases
# > High interest Rates leads to low original amount borrowed

# ## Multivariate Exploration
# <span id="mul"></span>
# 
# > Create plots of three or more variables to investigate your data even
# further. Make sure that your investigations are justified, and follow from
# your work in the previous sections.

# ### Pairplot in Examining Outlook Across All the Eight (8) Variables

# #### Question

# > - Is there any noticeable relationship across all the eight (8) variables of interest?

# #### Visualization

# In[34]:


sb.pairplot(focus_data[['LoanStatus', 'LoanOriginalAmount', 'BorrowerRate', 'Occupation',
                      'IncomeRange', 'EmploymentStatus', 'EstimatedReturn', 'EstimatedLoss']], diag_kind ='kde', corner= True);


# #### Observations

# > - In creating the pair plot based on Loan Status, it can be seen that for the members, some variables have clear association
# > - For BorrowerRate and EstimatedLoss and EstimatedReturn, the scatter plots shows positively association
# > - Rising BorrowerRate is positively associated/correlated to EstimatedLoss and EstimatedReturn
# > - For EstimatedLoss and EstimatedReturn, the correlation is negative, based on the scatter plots

# ### Examining Outlook Across All the Eight (8) Variables Relative to "LoanStatus"

# #### Question

# > - How does LoanStatus impact on all the eight (8) variables of interest?

# #### Visualization

# In[35]:


# The 'hue' element was added in examining the interest variables based on 'LoanStatus'
sb.pairplot(focus_data[['LoanStatus', 'LoanOriginalAmount', 'BorrowerRate', 'Occupation',
                      'IncomeRange', 'EmploymentStatus', 'EstimatedReturn', 'EstimatedLoss']], hue = 'LoanStatus');


# #### Observation

# > - In creating the pair plot based on Loan Status, it can be seen that for the members, impact varies based on scatter plots
# > - Current LoanStatus has the most impact on EstimatedLoss, EstimatedReturn, BorrowRate and LoanOriginalAmount
# > - Across Loan Status, BorrowerRate, EstimatedReturn, and EstimatedLoss have a positive correlation

# ### Correlation Between Continuous Variables

# #### Question

# > - Are there insights across the quantiative variables selected for examination in the dataset?

# #### Visulaiization

# > In making the exploration, five variables are chosen, with the adoption of a heatmap() for visualization. 
# > - These are: 
# > 1. 'LoanOriginalAmount',
# > 2. 'BorrowerRate',
# > 3. 'EstimatedReturn', & 
# > 4. 'EstimatedLoss'

# In[36]:


# In checking association, adopting correlation is used in this section
# Correlation technique is used in this case
# First, defining the dataset
correlation_data = loan_data[['LoanOriginalAmount', 'BorrowerRate', 'Occupation', 'EstimatedReturn', 'EstimatedLoss']]

# Setting the plot's size 
plt.figure(figsize = [10, 8])
# Visualization and reporting results to 2 decimal places
sb.heatmap(correlation_data.corr(), annot = True, fmt = '.2f',
           cmap = 'vlag_r', center = 0)
plt.title('Correlation Between the Four (4) Pre-Chosen Variables')
bottom, top = plt.ylim() 
bottom += 0.5 
top -= 0.5
plt.ylim(bottom, top)
plt.yticks(rotation=0);
plt.show()


# #### Observation

# > - Of the 5 variables, LoanOriginalAmount has negative correlation with BorrowerRate (-0.33), EstimatedLoss (- 0.43), EstimatedReturn (-0.29)
# > - BorrowerRate has positive correlation with EstimatedLoss (0.95), EstimatedReturn (0.82), and negative for LoanOriginalAmount (-0.33)

# ### Saving The Cleaned Dataframe to a CSV file: This will be used in Explanatory Presentation

# In[37]:


# Name: slide_data
focus_data.to_csv("slide_data.csv")


# ## Conclusions
# <span id="conc"></span>
# 
# > The exploration focuses on Prosper Loan Data comprising 81 columns and 113,937 rows. Of the diverse variables, this exploration focused on eight (8) variables, i.e., LoanStatus", "LoanOriginalAmount", "BorrowerRate", "Occupation", "IncomeRange", "EmploymentStatus", "EstimatedReturn" and EstimatedLoss". On loan status, current and completed were the two most occurences, with cancelled as the least. Secondly, on Loan Original amount, the distribution was somehow normal despite skewness in the dataset, with most amount being 4000, 15000 and 100000 for borrowers. The borrower rate (interest) rate was normally distributed with the most used rate being between 0.1 to 0.2. Top profession were Professional and computer programmer and executive. The multivariate analysis showed positive association across the variables, including Income Range and Loan status based on boxplots. Also, by checking correlation across quantitative variables (numeric), there were differences in correlation coefficient. Of the 5 variables, LoanOriginalAmount has negative correlation with BorrowerRate (-0.33), EstimatedLoss (-0.43), EstimatedReturn (-0.29). BorrowerRate has positive correlation with EstimatedLoss (0.95), EstimatedReturn (0.82), and negative for LoanOriginalAmount (-0.33)

# ## References
# <span id="ref"></span>
# > 1. ALX-Udacity classroom videos and Notes. https://classroom.udacity.com/nanodegree
# > 2. Seaborn (202). seaborn: statistical data visualization. https://seaborn.pydata.org/index.html
# 
