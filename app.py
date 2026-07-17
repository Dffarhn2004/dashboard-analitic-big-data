import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Dashboard Evaluasi Pengalaman dan Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide",
)

SATISFACTION_ORDER = [
    "Very Satisfied",
    "Satisfied",
    "Neutral",
    "Dissatisfied",
    "Very Dissatisfied",
]
SATISFACTION_SCORE = {
    "Very Dissatisfied": 1,
    "Dissatisfied": 2,
    "Neutral": 3,
    "Satisfied": 4,
    "Very Satisfied": 5,
}
CATEGORY_ORDER = ["Puas", "Netral", "Tidak Puas"]
CATEGORY_COLORS = {
    "Puas": "#2E7D32",
    "Netral": "#9E9E9E",
    "Tidak Puas": "#C62828",
}
COUNTRY_ISO3 = {
    "Australia": "AUS",
    "Canada": "CAN",
    "China": "CHN",
    "France": "FRA",
    "Germany": "DEU",
    "India": "IND",
    "Japan": "JPN",
    "Malaysia": "MYS",
    "Netherlands": "NLD",
    "Pakistan": "PAK",
    "Turkey": "TUR",
    "UAE": "ARE",
    "UK": "GBR",
    "USA": "USA",
}
SATISFACTION_COLORS = {
    "Very Satisfied": "#1B5E20",
    "Satisfied": "#66BB6A",
    "Neutral": "#9E9E9E",
    "Dissatisfied": "#FB8C00",
    "Very Dissatisfied": "#C62828",
}
DISPLAY_COLUMNS = [
    "student_id",
    "age",
    "gender",
    "country",
    "program_level",
    "field_of_study",
    "year_of_study",
    "scholarship",
    "online_classes",
    "campus_facilities_rating",
    "teaching_quality_rating",
    "overall_satisfaction",
    "satisfaction_category",
]


def classify_satisfaction(value: str) -> str:
    if value in {"Satisfied", "Very Satisfied"}:
        return "Puas"
    if value == "Neutral":
        return "Netral"
    return "Tidak Puas"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/world_university_survey_dataset.csv")
    # Simpan sebagai string, bukan Categorical — Streamlit cache (pickle)
    # gagal unpickle Categorical pada beberapa versi pandas/Python.
    return df.assign(
        satisfaction_score=df["overall_satisfaction"].map(SATISFACTION_SCORE),
        satisfaction_category=df["overall_satisfaction"].map(classify_satisfaction),
    )


def init_filters(df: pd.DataFrame) -> None:
    defaults = {
        "program_level": sorted(df["program_level"].unique()),
        "field_of_study": sorted(df["field_of_study"].unique()),
        "year_of_study": sorted(df["year_of_study"].unique()),
        "scholarship": sorted(df["scholarship"].unique()),
        "online_classes": sorted(df["online_classes"].unique()),
        "country": sorted(df["country"].unique()),
        "gender": sorted(df["gender"].unique()),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_filters(df: pd.DataFrame) -> None:
    st.session_state.program_level = sorted(df["program_level"].unique())
    st.session_state.field_of_study = sorted(df["field_of_study"].unique())
    st.session_state.year_of_study = sorted(df["year_of_study"].unique())
    st.session_state.scholarship = sorted(df["scholarship"].unique())
    st.session_state.online_classes = sorted(df["online_classes"].unique())
    st.session_state.country = sorted(df["country"].unique())
    st.session_state.gender = sorted(df["gender"].unique())


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Filter Data")
    st.caption(
        "Gunakan filter untuk membandingkan pengalaman mahasiswa berdasarkan "
        "jenjang, bidang studi, tahun studi, beasiswa, dan kelas daring."
    )

    row1 = st.columns(4)
    with row1[0]:
        st.multiselect(
            "Program Level",
            options=sorted(df["program_level"].unique()),
            key="program_level",
        )
    with row1[1]:
        st.multiselect(
            "Field of Study",
            options=sorted(df["field_of_study"].unique()),
            key="field_of_study",
        )
    with row1[2]:
        st.multiselect(
            "Year of Study",
            options=sorted(df["year_of_study"].unique()),
            key="year_of_study",
        )
    with row1[3]:
        st.multiselect(
            "Scholarship",
            options=sorted(df["scholarship"].unique()),
            key="scholarship",
        )

    row2 = st.columns(4)
    with row2[0]:
        st.multiselect(
            "Online Classes",
            options=sorted(df["online_classes"].unique()),
            key="online_classes",
        )
    with row2[1]:
        st.multiselect(
            "Country of Origin",
            options=sorted(df["country"].unique()),
            key="country",
        )
    with row2[2]:
        st.multiselect(
            "Gender",
            options=sorted(df["gender"].unique()),
            key="gender",
        )
    with row2[3]:
        st.write("")
        st.write("")
        st.button(
            "Reset Filter",
            on_click=reset_filters,
            args=(df,),
            use_container_width=True,
        )

    required = [
        st.session_state.program_level,
        st.session_state.field_of_study,
        st.session_state.year_of_study,
        st.session_state.scholarship,
        st.session_state.online_classes,
        st.session_state.country,
        st.session_state.gender,
    ]
    if any(len(value) == 0 for value in required):
        st.warning("Pilih minimal satu nilai pada setiap filter.")
        st.stop()

    return df[
        df["program_level"].isin(st.session_state.program_level)
        & df["field_of_study"].isin(st.session_state.field_of_study)
        & df["year_of_study"].isin(st.session_state.year_of_study)
        & df["scholarship"].isin(st.session_state.scholarship)
        & df["online_classes"].isin(st.session_state.online_classes)
        & df["country"].isin(st.session_state.country)
        & df["gender"].isin(st.session_state.gender)
    ].copy()


def render_kpi(filtered_df: pd.DataFrame) -> None:
    total = len(filtered_df)
    if total == 0:
        st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        st.stop()

    pct_satisfied = (
        filtered_df["satisfaction_category"].eq("Puas").sum() / total * 100
    )
    pct_dissatisfied = (
        filtered_df["satisfaction_category"].eq("Tidak Puas").sum() / total * 100
    )
    avg_teaching = filtered_df["teaching_quality_rating"].mean()
    avg_facilities = filtered_df["campus_facilities_rating"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Responden", f"{total:,}".replace(",", "."))
    c2.metric("Mahasiswa Puas", f"{pct_satisfied:.1f}%")
    c3.metric("Mahasiswa Tidak Puas", f"{pct_dissatisfied:.1f}%")
    c4.metric("Rata-rata Kualitas Pengajaran", f"{avg_teaching:.2f} / 5")
    c5.metric("Rata-rata Fasilitas Kampus", f"{avg_facilities:.2f} / 5")


def satisfaction_distribution_chart(filtered_df: pd.DataFrame):
    counts = (
        filtered_df["overall_satisfaction"]
        .value_counts()
        .reindex(SATISFACTION_ORDER)
        .fillna(0)
        .rename_axis("overall_satisfaction")
        .reset_index(name="jumlah")
    )
    counts = counts.assign(persen=counts["jumlah"] / counts["jumlah"].sum() * 100)

    fig = px.bar(
        counts,
        x="jumlah",
        y="overall_satisfaction",
        orientation="h",
        color="overall_satisfaction",
        color_discrete_map=SATISFACTION_COLORS,
        text=counts["persen"].map(lambda x: f"{x:.1f}%"),
        labels={
            "jumlah": "Jumlah Mahasiswa",
            "overall_satisfaction": "Tingkat Kepuasan",
        },
        category_orders={"overall_satisfaction": SATISFACTION_ORDER},
    )
    fig.update_layout(
        showlegend=False,
        yaxis={"categoryorder": "array", "categoryarray": SATISFACTION_ORDER[::-1]},
        margin=dict(l=20, r=20, t=30, b=20),
    )
    fig.update_traces(textposition="outside")
    return fig


def field_satisfaction_chart(filtered_df: pd.DataFrame):
    field_counts = (
        filtered_df.groupby(["field_of_study", "satisfaction_category"])
        .size()
        .reset_index(name="jumlah")
    )
    field_totals = field_counts.groupby("field_of_study")["jumlah"].transform("sum")
    field_counts = field_counts.assign(persen=field_counts["jumlah"] / field_totals * 100)

    order = (
        field_counts[field_counts["satisfaction_category"] == "Tidak Puas"]
        .sort_values("persen", ascending=False)["field_of_study"]
        .tolist()
    )
    missing = [
        field
        for field in sorted(filtered_df["field_of_study"].unique())
        if field not in order
    ]
    order = order + missing

    fig = px.bar(
        field_counts,
        x="persen",
        y="field_of_study",
        color="satisfaction_category",
        orientation="h",
        color_discrete_map=CATEGORY_COLORS,
        category_orders={
            "field_of_study": order,
            "satisfaction_category": CATEGORY_ORDER,
        },
        labels={
            "persen": "Proporsi (%)",
            "field_of_study": "Bidang Studi",
            "satisfaction_category": "Kategori",
        },
    )
    fig.update_layout(
        barmode="stack",
        barnorm="percent",
        legend_title_text="",
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def teaching_facilities_by_field_chart(filtered_df: pd.DataFrame):
    summary = (
        filtered_df.groupby("field_of_study", as_index=False)
        .agg(
            teaching_quality_rating=("teaching_quality_rating", "mean"),
            campus_facilities_rating=("campus_facilities_rating", "mean"),
        )
        .melt(
            id_vars="field_of_study",
            value_vars=["teaching_quality_rating", "campus_facilities_rating"],
            var_name="indikator",
            value_name="rata_rata",
        )
    )
    summary = summary.assign(
        indikator=summary["indikator"].map(
            {
                "teaching_quality_rating": "Kualitas Pengajaran",
                "campus_facilities_rating": "Fasilitas Kampus",
            }
        )
    )

    avg_teaching = filtered_df["teaching_quality_rating"].mean()
    avg_facilities = filtered_df["campus_facilities_rating"].mean()

    fig = px.bar(
        summary,
        x="rata_rata",
        y="field_of_study",
        color="indikator",
        barmode="group",
        orientation="h",
        labels={
            "rata_rata": "Rata-rata (skala 1–5)",
            "field_of_study": "Bidang Studi",
            "indikator": "Indikator",
        },
        color_discrete_sequence=["#1565C0", "#00897B"],
    )
    fig.add_vline(
        x=avg_teaching,
        line_dash="dash",
        line_color="#1565C0",
        annotation_text="Rata-rata pengajaran",
        annotation_position="top",
    )
    fig.add_vline(
        x=avg_facilities,
        line_dash="dot",
        line_color="#00897B",
        annotation_text="Rata-rata fasilitas",
        annotation_position="bottom",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), xaxis=dict(range=[1, 5]))
    return fig


def rating_satisfaction_heatmap(
    filtered_df: pd.DataFrame,
    rating_col: str,
    title: str,
):
    heat = (
        filtered_df.groupby([rating_col, "overall_satisfaction"])
        .size()
        .reset_index(name="jumlah")
    )
    pivot = (
        heat.pivot(index=rating_col, columns="overall_satisfaction", values="jumlah")
        .reindex(index=[1, 2, 3, 4, 5], columns=SATISFACTION_ORDER)
        .fillna(0)
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=list(pivot.columns),
            y=[str(i) for i in pivot.index],
            colorscale="YlGnBu",
            text=pivot.values.astype(int),
            texttemplate="%{text}",
            hovertemplate=(
                "Rating %{y}<br>%{x}<br>Jumlah: %{z}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Tingkat Kepuasan",
        yaxis_title="Rating",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def stacked_group_chart(
    filtered_df: pd.DataFrame,
    group_col: str,
    labels: dict[str, str],
):
    counts = (
        filtered_df.groupby([group_col, "satisfaction_category"])
        .size()
        .reset_index(name="jumlah")
    )
    totals = counts.groupby(group_col)["jumlah"].transform("sum")
    counts = counts.assign(
        persen=counts["jumlah"] / totals * 100,
        **{group_col: counts[group_col].map(labels).fillna(counts[group_col])},
    )

    fig = px.bar(
        counts,
        x=group_col,
        y="persen",
        color="satisfaction_category",
        color_discrete_map=CATEGORY_COLORS,
        category_orders={"satisfaction_category": CATEGORY_ORDER},
        labels={
            group_col: "",
            "persen": "Proporsi (%)",
            "satisfaction_category": "Kategori",
        },
        text=counts["persen"].map(lambda x: f"{x:.1f}%"),
    )
    fig.update_layout(
        barmode="stack",
        barnorm="percent",
        legend_title_text="",
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(range=[0, 100]),
    )
    fig.update_traces(textposition="inside")
    return fig


def priority_insight(filtered_df: pd.DataFrame) -> str:
    field_stats = (
        filtered_df.groupby("field_of_study", as_index=False)
        .agg(
            pct_tidak_puas=(
                "satisfaction_category",
                lambda s: (s == "Tidak Puas").mean() * 100,
            ),
            avg_teaching=("teaching_quality_rating", "mean"),
        )
    )
    uni_avg_teaching = filtered_df["teaching_quality_rating"].mean()
    priority = field_stats[
        (field_stats["pct_tidak_puas"] >= field_stats["pct_tidak_puas"].median())
        & (field_stats["avg_teaching"] < uni_avg_teaching)
    ].sort_values("pct_tidak_puas", ascending=False)

    if priority.empty:
        top = field_stats.sort_values("pct_tidak_puas", ascending=False).iloc[0]
        return (
            f"Bidang studi dengan proporsi ketidakpuasan tertinggi saat ini adalah "
            f"**{top['field_of_study']}** ({top['pct_tidak_puas']:.1f}%). "
            "Pola ini bersifat deskriptif dan perlu ditindaklanjuti dengan evaluasi lebih lanjut."
        )

    names = ", ".join(priority["field_of_study"].head(3).tolist())
    return (
        f"Bidang studi yang perlu menjadi prioritas evaluasi akademik: **{names}**. "
        "Kelompok ini memiliki proporsi mahasiswa tidak puas yang relatif tinggi "
        "serta penilaian kualitas pengajaran di bawah rata-rata universitas. "
        "Temuan ini tidak membuktikan hubungan sebab-akibat."
    )


def country_dissatisfaction_map(filtered_df: pd.DataFrame):
    country_stats = (
        filtered_df.groupby("country", as_index=False)
        .agg(
            jumlah=("student_id", "count"),
            pct_tidak_puas=(
                "satisfaction_category",
                lambda s: (s == "Tidak Puas").mean() * 100,
            ),
            pct_puas=(
                "satisfaction_category",
                lambda s: (s == "Puas").mean() * 100,
            ),
        )
    )
    country_stats = country_stats.assign(
        iso_alpha=country_stats["country"].map(COUNTRY_ISO3)
    ).dropna(subset=["iso_alpha"])

    fig = px.choropleth(
        country_stats,
        locations="iso_alpha",
        color="pct_tidak_puas",
        hover_name="country",
        hover_data={
            "iso_alpha": False,
            "jumlah": True,
            "pct_puas": ":.1f",
            "pct_tidak_puas": ":.1f",
        },
        color_continuous_scale="OrRd",
        labels={
            "pct_tidak_puas": "% Tidak Puas",
            "pct_puas": "% Puas",
            "jumlah": "Jumlah responden",
        },
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
        ),
        coloraxis_colorbar=dict(title="% Tidak Puas"),
    )
    return fig


def main() -> None:
    df = load_data()
    init_filters(df)

    st.title("Dashboard Evaluasi Pengalaman dan Kepuasan Mahasiswa")
    st.caption(
        "Memantau tingkat kepuasan mahasiswa dan mengidentifikasi aspek layanan "
        "akademik yang memerlukan peningkatan."
    )
    st.info(
        "Seluruh responden diposisikan sebagai mahasiswa dari satu universitas "
        "simulasi. Kolom negara menggambarkan asal mahasiswa; nama universitas "
        "pada dataset tidak digunakan dalam analisis."
    )

    filtered_df = render_filters(df)
    st.divider()
    render_kpi(filtered_df)
    st.divider()

    st.header("1. Kondisi Kepuasan Mahasiswa")
    col_sat, col_map = st.columns(2)
    with col_sat:
        st.subheader("Distribusi Tingkat Kepuasan")
        st.caption(
            "Grafik menunjukkan distribusi seluruh tingkat kepuasan, sehingga rektorat "
            "tidak hanya bergantung pada satu nilai rata-rata."
        )
        st.plotly_chart(
            satisfaction_distribution_chart(filtered_df),
            use_container_width=True,
        )
    with col_map:
        st.subheader("Peta negara asal mahasiswa")
        st.caption(
            "Peta menampilkan proporsi mahasiswa tidak puas berdasarkan negara asal. "
            "Ini bukan lokasi kampus, melainkan asal responden."
        )
        st.plotly_chart(
            country_dissatisfaction_map(filtered_df),
            use_container_width=True,
        )

    st.divider()
    st.header("2. Kelompok yang Memerlukan Perhatian")
    st.subheader("Bidang studi dengan proporsi mahasiswa tidak puas tertinggi")
    st.caption(
        "Proporsi digunakan agar perbandingan antarbidang studi tetap adil meskipun "
        "jumlah responden berbeda."
    )
    st.plotly_chart(field_satisfaction_chart(filtered_df), use_container_width=True)

    st.subheader("Kualitas pengajaran dan fasilitas per bidang studi")
    st.caption(
        "Garis referensi menunjukkan rata-rata universitas agar bidang di bawah "
        "rata-rata lebih mudah dikenali."
    )
    st.plotly_chart(
        teaching_facilities_by_field_chart(filtered_df),
        use_container_width=True,
    )
    st.success(priority_insight(filtered_df))

    st.divider()
    st.header("3. Faktor yang Berkaitan dengan Kepuasan")
    left, right = st.columns(2)
    with left:
        st.subheader("Kualitas pengajaran vs kepuasan")
        st.caption(
            "Ketika penilaian kualitas pengajaran meningkat, apakah distribusi "
            "kepuasan bergeser ke arah yang lebih positif?"
        )
        st.plotly_chart(
            rating_satisfaction_heatmap(
                filtered_df,
                "teaching_quality_rating",
                "Teaching Quality vs Satisfaction",
            ),
            use_container_width=True,
        )
    with right:
        st.subheader("Fasilitas kampus vs kepuasan")
        st.caption(
            "Apakah mahasiswa yang menilai fasilitas rendah juga cenderung lebih "
            "tidak puas?"
        )
        st.plotly_chart(
            rating_satisfaction_heatmap(
                filtered_df,
                "campus_facilities_rating",
                "Campus Facilities vs Satisfaction",
            ),
            use_container_width=True,
        )
    st.caption(
        "Pola di atas bersifat deskriptif dan tidak membuktikan hubungan sebab-akibat."
    )

    st.divider()
    st.header("4. Perbandingan Pengalaman Mahasiswa")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Kelas daring vs non-daring")
        st.caption(
            "Apakah mahasiswa yang mengikuti kelas daring menunjukkan distribusi "
            "kepuasan yang berbeda?"
        )
        st.plotly_chart(
            stacked_group_chart(
                filtered_df,
                "online_classes",
                {"Yes": "Online: Yes", "No": "Online: No"},
            ),
            use_container_width=True,
        )
    with col_b:
        st.subheader("Penerima vs nonpenerima beasiswa")
        st.caption(
            "Apakah pengalaman mahasiswa penerima beasiswa berbeda dari mahasiswa "
            "nonpenerima?"
        )
        st.plotly_chart(
            stacked_group_chart(
                filtered_df,
                "scholarship",
                {"Yes": "Scholarship: Yes", "No": "Scholarship: No"},
            ),
            use_container_width=True,
        )

    st.divider()
    st.header("5. Data Detail dan Catatan")
    st.dataframe(
        filtered_df[DISPLAY_COLUMNS].sort_values(
            ["field_of_study", "program_level", "student_id"]
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv = filtered_df[DISPLAY_COLUMNS].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Unduh Data Hasil Filter (CSV)",
        data=csv,
        file_name="data_kepuasan_mahasiswa_filtered.csv",
        mime="text/csv",
    )

    st.markdown(
        """
**Sumber:** World University Student Survey Dataset, Kaggle  
**Catatan:** Data bersifat sintetis. Hasil dashboard bersifat deskriptif dan tidak
dimaksudkan untuk membuktikan hubungan sebab-akibat.
"""
    )


if __name__ == "__main__":
    main()
