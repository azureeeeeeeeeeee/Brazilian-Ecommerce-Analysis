import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


bystate_df = pd.read_csv('data/customer_state.csv')
rfm_df = pd.read_csv('data/rfm.csv')
product_df = pd.read_csv('data/product_count.csv')
review_df = pd.read_csv('data/product_review_count2.csv')
revenue_df = pd.read_csv('data/revenue.csv')

# Memastikan bahwa kolom 'order_approved_at' memiliki tipe data 'datetime'
revenue_df['order_approved_at'] = pd.to_datetime(
    revenue_df['order_approved_at'])


# Membuat komponen range tanggal untuk digunakan di sidebar
min_date = revenue_df['order_approved_at'].min()
max_date = revenue_df['order_approved_at'].max()

with st.sidebar:
    st.text('Format:\n yyyy-mm-dd')
    # Membuat slider untuk menentukan range waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = revenue_df[(revenue_df['order_approved_at'] >= str(start_date))
                     & (revenue_df['order_approved_at'] <= str(end_date))]

st.header('E-Commerce Collection Dashboard :sparkles:')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.total_order.sum()
    st.metric('Total orders', value=total_orders)

with col2:
    total_revenue = format_currency(
        main_df.total_revenue.sum(), "BRL", locale='ES_CO'
    )
    st.metric('Total Revenue', value=total_revenue)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    revenue_df['order_approved_at'],
    revenue_df['total_order'],
    marker='o',
    linewidth=2,
    color='#90CAF9'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title('Total Revenue 2016/09 - 2018/07', fontsize=30)
st.pyplot(fig)


st.subheader('Best & Worst Performing Product\'s Category')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 12))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='total_order', y='product_category_name_english', data=product_df.groupby(
    'product_category_name_english').total_order.nunique().sort_values(ascending=False).reset_index().head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Best Performing Product)', fontsize=30)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x='total_order', y='product_category_name_english', data=product_df.groupby(
    'product_category_name_english').total_order.nunique().sort_values(ascending=True).reset_index().head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position('right')
ax[1].set_title('Worst Performing Product', fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)

plt.suptitle('Best & Worst Performing Product (By Sales)', fontsize=35)
st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 12))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='mean_review_score', y='product_category_name_english', data=review_df.sort_values(
    by='mean_review_score', ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Best Performing Product (By Review Score)', fontsize=30)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x='mean_review_score', y='product_category_name_english', data=review_df.sort_values(
    by='mean_review_score', ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position('right')
ax[1].set_title('Worst Performing Product (By Review Score)', fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)

plt.suptitle('Best & Worst Performing Product (By Review Score)', fontsize=35)
st.pyplot(fig)


st.subheader('Customer Demographics')

fig, ax = plt.subplots(figsize=(25, 10))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",
          "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='total_customer', y='customer_state',
            data=bystate_df, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title('Number of Customer by State', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25)

st.pyplot(fig)


st.subheader('Best Customer Based on RFM Parameters')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric('Average Recency (days)', value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric('Average Frequency', value=avg_frequency)

with col3:
    avg_monetary = format_currency(
        rfm_df.monetary.mean(), 'BRL', locale='es_CO')
    st.metric('Average Monetary', value=avg_monetary)

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(
    x='recency',
    y='customer_id',
    data=rfm_df.sort_values('recency', ascending=True).head(5),
    palette=colors,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title('By Recency (days)', loc='center', fontsize=50)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(
    x='recency',
    y='customer_id',
    data=rfm_df.sort_values('frequency', ascending=True).head(5),
    palette=colors,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title('By Frequency', loc='center', fontsize=50)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig)


fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(
    x='recency',
    y='customer_id',
    data=rfm_df.sort_values('recency', ascending=True).head(5),
    palette=colors,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title('By Monetary', loc='center', fontsize=50)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig)


st.caption('Copyright (c) Dicoding 2023')


# Copyright untuk dicoding, karena saya kebanyakan liat dari projek lama saya
