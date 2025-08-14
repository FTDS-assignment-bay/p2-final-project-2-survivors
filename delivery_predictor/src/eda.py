import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import streamlit as st
from pathlib import Path

def run():
    # header
    st.header("Delivery Status Prediction")
    st.markdown('---')

    # section dataframe
    df = pd.read_csv('C:\\Users\\User\\p2-final_project\\p2-final-project-2-survivors\\delivery_predictor\\src\\cleaned_data.csv')
    st.dataframe(df.head(10))
    st.markdown('---')

     # section visualization
    st.subheader("Visualizations")

    # 1. Bar Plot for Class Balance
    ontime = pd.to_numeric(df["reached_on_time"], errors="coerce").fillna(1).clip(0, 1).astype(int)
    status = ontime.map({1: "On-Time", 0: "Late"})

    # --- Hitung jumlah per status & urutkan Late -> On-Time ---
    plot_df = (status.value_counts()
                    .reindex(["Late", "On-Time"])
                    .fillna(0).astype(int)
                    .reset_index())
    plot_df.columns = ["Delivery_Status", "Count"]

    # Label angka dengan pemisah ribuan titik (4.436)
    labels_text = plot_df["Count"].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    # --- Plot ---
    fig = px.bar(
        plot_df,
        x="Delivery_Status",
        y="Count",
        text=labels_text,
        labels={"Delivery_Status": "Delivery_Status", "Count": "Count of Deliveries"},
        title="1. Delivery Status (Class Balance)",
    )
    fig.update_traces(textposition="outside")
    fig.update_yaxes(tickformat="~s", title_text="Count of Deliveries")
    fig.update_layout(showlegend=False, margin=dict(t=60, r=20, b=20, l=60))

    st.plotly_chart(fig, use_container_width=True)
    st.write("Keterlambatan yang mencapai 40% tergolong medium, dan harus diperbaiki.")


    # 2. horizontal bar plot for late rate by warehouse
    status_col = None
    for cand in ["reached on time", "reached_on_time", "Reached.on.Time_Y.N"]:
        if cand in df.columns:
            status_col = cand
            break
    if status_col is None:
        st.error("Kolom status tidak ditemukan. Harus ada 'reached on time' (atau 'reached_on_time').")
        st.stop()

    # warehouse_block
    warehouse_col = "warehouse_block" if "warehouse_block" in df.columns else \
                    ("Warehouse_block" if "Warehouse_block" in df.columns else None)
    if warehouse_col is None:
        st.error("Kolom 'warehouse_block' tidak ditemukan.")
        st.stop()

    # Hitung late rate per warehouse
    ontime = pd.to_numeric(df[status_col], errors="coerce").fillna(1).clip(0, 1).astype(int)
    late_flag = 1 - ontime  # 1=Late, 0=On-Time

    g = (pd.DataFrame({warehouse_col: df[warehouse_col], "late": late_flag})
            .groupby(warehouse_col, as_index=False)
            .agg(late_rate=("late", "mean"), n=("late", "size"))
            .sort_values("late_rate", ascending=False))

    # Plot bar horizontal + label persen + judul
    fig2 = px.bar(
        g,
        x="late_rate",
        y=warehouse_col,
        orientation="h",
        text=(g["late_rate"]*100).round(1).astype(str).str.replace(".", ",") + "%",
        labels={warehouse_col: "Warehouse", "late_rate": "Late_Rate"},
        title="2. Late Rate by Warehouse",
        color="late_rate" 
    )
    fig2.update_xaxes(range=[0, 1], tickformat=".0%")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(showlegend=False, margin=dict(t=60, r=20, b=20, l=60))

    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Late dihitung dari 'reached on time' (1 = On-Time, 0 = Late).")
    st.write("Tingkat keterlambatan bervariasi antar gudang, dengan gudang A paling tinggi (41,4%) dan gudang B paling rendah (39,8%).")

    # 3. bar plot for late rate by mode of shipment
    status_col = None
    for c in ["reached_on_time", "reached on time", "Reached.on.Time_Y.N"]:
        if c in df.columns:
            status_col = c
            break
    if status_col is None:
        st.error("Kolom status tidak ditemukan. Gunakan 'reached_on_time' / 'reached on time'.")
        st.stop()

    # Kolom mode pengiriman
    mode_col = "mode_of_shipment" if "mode_of_shipment" in df.columns else None
    if mode_col is None:
        st.error("Kolom 'mode_of_shipment' tidak ditemukan.")
        st.stop()

    # Hitung late rate per mode
    ontime = pd.to_numeric(df[status_col], errors="coerce").fillna(1).clip(0, 1).astype(int)
    late_flag = 1 - ontime  # 1=Late, 0=On-Time

    g = (
        pd.DataFrame({mode_col: df[mode_col], "late": late_flag})
        .groupby(mode_col, as_index=False)
        .agg(late_rate=("late", "mean"), n=("late", "size"))
    )

    # urutkan kategori: Road, Ship, Flight
    order = ["Road", "Ship", "Flight"]
    g[mode_col] = pd.Categorical(g[mode_col], categories=order, ordered=True)
    g = g.sort_values(mode_col)

    # Plot bar vertikal + judul + sumbu persen dengan koma
    fig3 = px.bar(
        g, x=mode_col, y="late_rate",
        labels={mode_col: "Mode of Shipment", "late_rate": "Late_Rate"},
        title="3. Late Rate by Mode of Shipment",
        color=mode_col,  # memberi warna berbeda per mode
        color_discrete_sequence=["#b61e37", "#ff8f4a", "#f1d373"] 
    )
    # y-axis pakai 0–50% dan format persen dengan koma
    fig3.update_yaxes(range=[0, 0.5], tickvals=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                    ticktext=["0,0%","10,0%","20,0%","30,0%","40,0%","50,0%"],
                    title_text="Late_Rate")
    fig3.update_layout(showlegend=False, margin=dict(t=60, r=20, b=20, l=60))

    st.plotly_chart(fig3, use_container_width=True)
    st.write("Moda Road sedikit lebih tinggi, tapi ketiga moda (Road/Ship/Flight) serupa sekitar 40%.")

    # 4. pie chart for share of late by mode of shipment
    g = None

    status_col = next((c for c in ["reached_on_time", "reached on time", "Reached.on.Time_Y.N"] if c in df.columns), None)
    if status_col is not None:
        ontime = pd.to_numeric(df[status_col], errors="coerce").fillna(1).clip(0, 1).astype(int)
        late_flag = 1 - ontime  # 1 = Late, 0 = On-Time
        g = (pd.DataFrame({mode_col: df[mode_col], "late": late_flag})
            .groupby(mode_col, as_index=False)
            .agg(late_count=("late", "sum")))

    if g is None:
        # cari rate dan ukuran sampel
        rate_col = next((c for c in ["late_rate", "Late_Rate", "late%"] if c in df.columns), None)
        n_col = next((c for c in ["n", "count", "Count", "total", "Total", "records", "Records"] if c in df.columns), None)
        if (rate_col is not None) and (n_col is not None):
            rate = pd.to_numeric(df[rate_col].astype(str).str.replace("%","").str.replace(",", "."), errors="coerce")
            # jika rate berupa persen (0–100), ubah ke 0–1
            rate = np.where(rate > 1, rate/100.0, rate)
            n = pd.to_numeric(df[n_col], errors="coerce")
            g = (pd.DataFrame({mode_col: df[mode_col], "late_count": rate * n})
                .groupby(mode_col, as_index=False)
                .agg(late_count=("late_count", "sum")))

    if g is None and "late_count" in df.columns:
        g = df.groupby(mode_col, as_index=False).agg(late_count=("late_count", "sum"))

    if g is None:
        st.error("Tidak dapat membentuk 'late_count'. Pastikan ada salah satu: "
                "1) kolom on-time (reached_on_time), atau 2) pasangan 'late_rate' + 'n'.")
        st.stop()

    g["late_count"] = pd.to_numeric(g["late_count"], errors="coerce").fillna(0).clip(lower=0)

    # Urutkan
    order = ["Flight", "Road", "Ship"]
    color_map = {"Flight": "#7BC87C", "Road": "#F7A64A", "Ship": "#5B83B1"}
    if set(order).issuperset(set(g[mode_col].unique())):
        g[mode_col] = pd.Categorical(g[mode_col], categories=order, ordered=True)
        g = g.sort_values(mode_col)

    total_late = g["late_count"].sum()
    if total_late <= 0:
        st.warning("Tidak ada kiriman Late pada data ini.")
        st.stop()
    labels = g[mode_col].astype(str) + " " + (g["late_count"]/total_late*100).round(2).astype(str).str.replace(".", ",") + "%"

    # Pie chart + judul
    fig4 = px.pie(
        g,
        names=mode_col,
        values="late_count",
        title="4. Share of Late by Mode of Shipment",
        color=mode_col,
        category_orders={mode_col: order},
        color_discrete_map=color_map
    )
    fig4.update_traces(text=labels, textinfo="text", textposition="outside")
    fig4.update_layout(
        legend=dict(title="Mode of Shipment", x=0.02, y=0.5),
        margin=dict(t=60, r=20, b=20, l=20),
        showlegend=True
    )

    st.plotly_chart(fig4, use_container_width=True)
    st.write("Sebagian besar kiriman terlambat terjadi via Ship (67,7%), diikuti Road dan Flight.")

    # 5. bar plot for late rate by product importance
    imp_col = "product_importance" if "product_importance" in df.columns else None

    if imp_col is None:
        st.error("Kolom 'Product_importance' tidak ditemukan.")
        st.stop()
    ontime = pd.to_numeric(df[status_col], errors="coerce").fillna(1).clip(0, 1).astype(int)
    late_flag = 1 - ontime  # 1=Late, 0=On-Time

    # Agregasi late rate per importance
    g = (
        pd.DataFrame({imp_col: df[imp_col].astype(str).str.lower(), "late": late_flag})
        .groupby(imp_col, as_index=False)
        .agg(late_rate=("late", "mean"))
    )

    # Urutan kategori: medium, low, high
    order = ["medium", "low", "high"]
    g[imp_col] = pd.Categorical(g[imp_col], categories=order, ordered=True)
    g = g.sort_values(imp_col)

    # Warna: medium & low merah, high kuning
    color_map = {"medium": "#b61e37", "low": "#b61e37", "high": "#f1d373"}

    # Plot bar
    fig5 = px.bar(
        g, x=imp_col, y="late_rate",
        labels={imp_col: "Product importance", "late_rate": "Late_Rate"},
        title="5. Late Rate by Product Importance",
        color=imp_col,
        category_orders={imp_col: order},
        color_discrete_map=color_map
    )
    # Sumbu Y ke persen dengan koma
    fig5.update_yaxes(
        range=[0, 0.5],
        tickvals=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
        ticktext=["0,0%","10,0%","20,0%","30,0%","40,0%","50,0%"],
        title_text="Late_Rate"
    )
    fig5.update_layout(showlegend=False, margin=dict(t=60, r=20, b=20, l=60))

    st.plotly_chart(fig5, use_container_width=True)
    st.write("Produk dengan Medium Importance memiliki tingkat keterlambatan tertinggi (41,0%), diikuti oleh Low dan High.")

    # 6. line plot for late rate by weight
    weight = pd.to_numeric(df["weight_in_gms"], errors="coerce")
    ontime = pd.to_numeric(df["reached_on_time"], errors="coerce")  # 1 on-time, 0 late
    late   = (1 - ontime).clip(lower=0, upper=1)  # 1=Late, 0=On-Time

    mask = weight.notna() & late.notna()
    weight, late = weight[mask], late[mask]

    # Binning 500g (bisa diubah dari sidebar)
    step = st.sidebar.number_input("Ukuran bin (gram)", min_value=100, max_value=5000, value=500, step=100)

    start = int(np.floor(weight.min()/step) * step)
    end   = int(np.ceil(weight.max()/step) * step) + step
    bins  = np.arange(start, end + step, step)

    cats = pd.cut(weight, bins=bins, right=False, include_lowest=True)
    mid  = cats.apply(lambda iv: iv.left + step/2)

    g = (pd.DataFrame({"mid": mid, "late": late})
        .groupby("mid")
        .agg(late_rate=("late", "mean"), n=("late", "size"))
        .reset_index())

    # Plot garis + label persen
    fig6 = px.line(g, x="mid", y="late_rate", markers=True,
                labels={"mid": f"Weight_Bin_Midpoint_{step}_G", "late_rate": "Late_Rate"},
                title="6. Late Rate by Weight"
               )
    fig6.update_yaxes(range=[0, 1], tickformat=".0%")
    labels = (g["late_rate"]*100).round(1).astype(str).str.replace(".", ",") + "%"
    fig6.update_traces(text=labels, textposition="top center")

    st.plotly_chart(fig6, use_container_width=True)
    st.caption("Late dihitung dari 'Reached.on.Time_Y.N' (1 = On-Time, 0 = Late).")
    st.write("Tingkat keterlambatan tertinggi terjadi di kisaran 4,5–6 kg, dan sangat rendah di luar rentang itu.")

    # 7. line plot for late rate by discount
    discount = pd.to_numeric(df["discount_offered"], errors="coerce")
    ontime = pd.to_numeric(df["reached_on_time"], errors="coerce").clip(0, 1)
    late = (1 - ontime)  # 1=Late, 0=On-Time

    mask = discount.notna() & late.notna()
    discount, late = discount[mask], late[mask]

    # Binning diskon: ukuran bin = 5
    step = 5
    start = np.floor(discount.min()/step) * step
    end   = np.ceil(discount.max()/step) * step + step
    bins  = np.arange(start, end + step, step)

    cats = pd.cut(discount, bins=bins, right=False, include_lowest=True)
    mid  = cats.apply(lambda iv: iv.left + step/2)

    g = (pd.DataFrame({"mid": mid, "late": late})
        .groupby("mid")
        .mean(numeric_only=True)
        .reset_index()
        .rename(columns={"late": "late_rate"})
        .sort_values("mid"))

    # Plot + label persen (53,6%)
    fig7 = px.line(g, x="mid", y="late_rate", markers=True,
                labels={"mid": "Discount_Midpoint", "late_rate": "Late_Rate"},
                title="7. Late Rate by Discount"
               )
    fig7.update_yaxes(range=[0, 1], tickformat=".0%")
    labels = (g["late_rate"]*100).round(1).astype(str).str.replace(".", ",") + "%"
    fig7.update_traces(text=labels, textposition="top center")
    fig7.update_layout(showlegend=False)

    st.plotly_chart(fig7, use_container_width=True)
    st.caption("Late dihitung dari 'Reached.on.Time_Y.N' (1 = On-Time, 0 = Late).")
    st.write("Keterlambatan tinggi pada diskon rendah (≤15%) dan turun hampir nol mulai sekitar diskon 20%.")

    # 8. line plot for late rate by calls
    calls = pd.to_numeric(df["customer_care_calls"], errors="coerce")
    ontime = pd.to_numeric(df["reached_on_time"], errors="coerce")  # 1=On-Time, 0=Late
    late = (1 - ontime)  # 1=Late, 0=On-Time

    mask = calls.notna() & late.notna()
    calls, late = calls[mask].astype(int), late[mask].clip(0, 1)

    g = (
        pd.DataFrame({"Calls": calls, "Late": late})
        .groupby("Calls", as_index=False)
        .agg(late_rate=("Late", "mean"), n=("Late", "size"))
        .sort_values("Calls")
    )

    # Plot garis + label persentase (34,8% dst)
    fig8 = px.line(
        g, x="Calls", y="late_rate", markers=True,
        labels={"Calls": "Calls", "late_rate": "Late_Rate"},
        title="8. Late Rate by Calls"
    )
    fig8.update_yaxes(range=[0, 1], tickformat=".0%")
    labels = (g["late_rate"] * 100).round(1).astype(str).str.replace(".", ",") + "%"
    fig8.update_traces(text=labels, textposition="top center")
    fig8.update_layout(showlegend=False, margin=dict(t=40, r=20, b=20, l=60))

    st.plotly_chart(fig8, use_container_width=True)
    st.caption("Late dihitung dari 'Reached.on.Time_Y.N' (1 = On-Time, 0 = Late).")
    st.write("Tingkat keterlambatan tertinggi terjadi pada pelanggan yang melakukan 4-6 panggilan, dan sangat rendah pada pelanggan yang tidak melakukan panggilan sama sekali.")
    st.write("Ini berarti bahwa semakin banyak panggilan yang dilakukan pelanggan, semakin tinggi kemungkinan keterlambatan pengiriman.")

if __name__ == "__main__":
    run()
