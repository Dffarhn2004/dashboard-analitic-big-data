import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Dashboard Evaluasi Pengalaman dan Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
    span[data-baseweb="tag"] {
        background-color: #E3F2FD !important;
        color: #0D47A1 !important;
    }
    span[data-baseweb="tag"] span[role="img"] {
        color: #0D47A1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
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
DISPLAY_COLUMN_LABELS = {
    "student_id": "ID Mahasiswa",
    "age": "Usia",
    "gender": "Jenis Kelamin",
    "country": "Negara Asal",
    "program_level": "Jenjang",
    "field_of_study": "Bidang Studi",
    "year_of_study": "Tahun Studi",
    "scholarship": "Penerima Beasiswa",
    "online_classes": "Kelas Daring",
    "campus_facilities_rating": "Nilai Fasilitas",
    "teaching_quality_rating": "Nilai Pengajaran",
    "overall_satisfaction": "Kepuasan Keseluruhan",
    "satisfaction_category": "Kategori Kepuasan",
}
MIN_SAMPLE_WARNING = 10


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
        "bidang studi, tahun studi, kelas daring, dan beasiswa."
    )

    row1 = st.columns([1, 1, 1, 1, 0.7])
    with row1[0]:
        st.multiselect(
            "Bidang Studi",
            options=sorted(df["field_of_study"].unique()),
            key="field_of_study",
        )
    with row1[1]:
        st.multiselect(
            "Tahun Studi",
            options=sorted(df["year_of_study"].unique()),
            key="year_of_study",
        )
    with row1[2]:
        st.multiselect(
            "Kelas Daring",
            options=sorted(df["online_classes"].unique()),
            format_func=lambda x: {"Yes": "Daring", "No": "Non-daring"}.get(x, x),
            key="online_classes",
        )
    with row1[3]:
        st.multiselect(
            "Beasiswa",
            options=sorted(df["scholarship"].unique()),
            format_func=lambda x: {"Yes": "Penerima", "No": "Nonpenerima"}.get(x, x),
            key="scholarship",
        )
    with row1[4]:
        st.write("")
        st.write("")
        st.button(
            "Reset Filter",
            on_click=reset_filters,
            args=(df,),
            use_container_width=True,
        )

    with st.expander("Filter lanjutan"):
        adv = st.columns(3)
        with adv[0]:
            st.multiselect(
                "Jenjang Pendidikan",
                options=sorted(df["program_level"].unique()),
                key="program_level",
            )
        with adv[1]:
            st.multiselect(
                "Negara Asal",
                options=sorted(df["country"].unique()),
                key="country",
            )
        with adv[2]:
            st.multiselect(
                "Jenis Kelamin",
                options=sorted(df["gender"].unique()),
                key="gender",
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
    pct_neutral = (
        filtered_df["satisfaction_category"].eq("Netral").sum() / total * 100
    )
    pct_dissatisfied = (
        filtered_df["satisfaction_category"].eq("Tidak Puas").sum() / total * 100
    )
    avg_teaching = filtered_df["teaching_quality_rating"].mean()
    avg_facilities = filtered_df["campus_facilities_rating"].mean()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Responden", f"{total:,}".replace(",", "."))
    c2.metric("Mahasiswa Puas", f"{pct_satisfied:.1f}%")
    c3.metric("Mahasiswa Netral", f"{pct_neutral:.1f}%")
    c4.metric("Mahasiswa Tidak Puas", f"{pct_dissatisfied:.1f}%")
    c5.metric("Rata-rata Kualitas Pengajaran", f"{avg_teaching:.2f} / 5")
    c6.metric("Rata-rata Fasilitas Kampus", f"{avg_facilities:.2f} / 5")
    st.caption(
        "Puas = Satisfied + Very Satisfied · "
        "Tidak Puas = Dissatisfied + Very Dissatisfied · "
        "Netral = Neutral"
    )


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
    field_n = filtered_df.groupby("field_of_study").size().to_dict()
    field_totals = field_counts.groupby("field_of_study")["jumlah"].transform("sum")
    field_counts = field_counts.assign(
        persen=field_counts["jumlah"] / field_totals * 100,
        field_label=field_counts["field_of_study"].map(
            lambda f: f"{f} (n={field_n[f]})"
        ),
    )
    field_counts = field_counts.assign(
        text_label=field_counts.apply(
            lambda r: (
                f"{r['persen']:.1f}%"
                if r["satisfaction_category"] == "Tidak Puas"
                else ""
            ),
            axis=1,
        ),
    )

    order_fields = (
        field_counts[field_counts["satisfaction_category"] == "Tidak Puas"]
        .sort_values("persen", ascending=False)["field_of_study"]
        .tolist()
    )
    missing = [
        field
        for field in sorted(filtered_df["field_of_study"].unique())
        if field not in order_fields
    ]
    order_fields = order_fields + missing
    order_labels = [f"{f} (n={field_n[f]})" for f in order_fields]

    fig = px.bar(
        field_counts,
        x="persen",
        y="field_label",
        color="satisfaction_category",
        orientation="h",
        color_discrete_map=CATEGORY_COLORS,
        text="text_label",
        category_orders={
            "field_label": order_labels,
            "satisfaction_category": CATEGORY_ORDER,
        },
        labels={
            "persen": "Proporsi (%)",
            "field_label": "Bidang Studi",
            "satisfaction_category": "Kategori",
        },
        custom_data=["jumlah", "field_of_study"],
    )
    fig.update_traces(
        textposition="inside",
        hovertemplate=(
            "%{customdata[1]}<br>%{fullData.name}: %{x:.1f}% "
            "(n=%{customdata[0]})<extra></extra>"
        ),
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
            n=("student_id", "count"),
        )
    )
    melted = summary.melt(
        id_vars=["field_of_study", "n"],
        value_vars=["teaching_quality_rating", "campus_facilities_rating"],
        var_name="indikator",
        value_name="rata_rata",
    )
    melted = melted.assign(
        indikator=melted["indikator"].map(
            {
                "teaching_quality_rating": "Kualitas Pengajaran",
                "campus_facilities_rating": "Fasilitas Kampus",
            }
        ),
        field_label=melted.apply(
            lambda r: f"{r['field_of_study']} (n={r['n']})", axis=1
        ),
    )

    avg_teaching = filtered_df["teaching_quality_rating"].mean()
    avg_facilities = filtered_df["campus_facilities_rating"].mean()

    fig = px.bar(
        melted,
        x="rata_rata",
        y="field_label",
        color="indikator",
        barmode="group",
        orientation="h",
        labels={
            "rata_rata": "Rata-rata (skala 1–5)",
            "field_label": "Bidang Studi",
            "indikator": "Indikator",
        },
        color_discrete_sequence=["#1565C0", "#00897B"],
        custom_data=["n", "field_of_study"],
    )
    fig.update_traces(
        hovertemplate=(
            "%{customdata[1]}<br>%{fullData.name}: %{x:.2f} "
            "(n=%{customdata[0]})<extra></extra>"
        )
    )
    fig.add_vline(
        x=avg_teaching,
        line_dash="dash",
        line_color="#1565C0",
        annotation_text=f"Rata-rata pengajaran ({avg_teaching:.2f})",
        annotation_position="top left",
    )
    fig.add_vline(
        x=avg_facilities,
        line_dash="dot",
        line_color="#00897B",
        annotation_text=f"Rata-rata fasilitas ({avg_facilities:.2f})",
        annotation_position="bottom right",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), xaxis=dict(range=[1, 5]))
    return fig


def rating_satisfaction_heatmap(
    filtered_df: pd.DataFrame,
    rating_col: str,
    title: str,
):
    pivot = (
        pd.crosstab(
            filtered_df[rating_col],
            filtered_df["overall_satisfaction"],
            normalize="index",
        )
        .reindex(index=[1, 2, 3, 4, 5], columns=SATISFACTION_ORDER)
        .fillna(0)
        * 100
    )
    row_n = (
        filtered_df.groupby(rating_col)
        .size()
        .reindex([1, 2, 3, 4, 5])
        .fillna(0)
        .astype(int)
    )
    text = pivot.map(lambda x: f"{x:.1f}%")
    customdata = [[int(row_n.loc[idx])] * len(pivot.columns) for idx in pivot.index]

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=list(pivot.columns),
            y=[str(i) for i in pivot.index],
            colorscale="YlGnBu",
            zmin=0,
            zmax=100,
            text=text.values,
            texttemplate="%{text}",
            customdata=customdata,
            hovertemplate=(
                "Rating %{y} (n=%{customdata})<br>%{x}<br>"
                "Proporsi: %{z:.1f}%<extra></extra>"
            ),
            colorbar=dict(title="Proporsi responden<br>pada setiap rating (%)"),
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
    group_n = filtered_df.groupby(group_col).size().to_dict()
    totals = counts.groupby(group_col)["jumlah"].transform("sum")
    counts = counts.assign(
        persen=counts["jumlah"] / totals * 100,
        group_label=counts[group_col].map(
            lambda v: f"{labels.get(v, v)} (n={group_n[v]})"
        ),
    )

    fig = px.bar(
        counts,
        x="group_label",
        y="persen",
        color="satisfaction_category",
        color_discrete_map=CATEGORY_COLORS,
        category_orders={"satisfaction_category": CATEGORY_ORDER},
        labels={
            "group_label": "",
            "persen": "Proporsi (%)",
            "satisfaction_category": "Kategori",
        },
        text=counts["persen"].map(lambda x: f"{x:.1f}%"),
        custom_data=["jumlah"],
    )
    fig.update_layout(
        barmode="stack",
        barnorm="percent",
        legend_title_text="",
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(range=[0, 100]),
    )
    fig.update_traces(
        textposition="inside",
        hovertemplate=(
            "%{x}<br>%{fullData.name}: %{y:.1f}% "
            "(n=%{customdata[0]})<extra></extra>"
        ),
    )
    return fig


def category_share(filtered_df: pd.DataFrame, mask: pd.Series, category: str) -> float:
    subset = filtered_df.loc[mask]
    if len(subset) == 0:
        return 0.0
    return subset["satisfaction_category"].eq(category).mean() * 100


def online_classes_insight(filtered_df: pd.DataFrame) -> str:
    online = filtered_df["online_classes"].eq("Yes")
    offline = filtered_df["online_classes"].eq("No")
    puas_online = category_share(filtered_df, online, "Puas")
    puas_offline = category_share(filtered_df, offline, "Puas")
    tidak_online = category_share(filtered_df, online, "Tidak Puas")
    tidak_offline = category_share(filtered_df, offline, "Tidak Puas")
    gap = abs(tidak_online - tidak_offline)
    return (
        f"Distribusi kepuasan mahasiswa daring dan non-daring relatif serupa. "
        f"Persentase mahasiswa puas masing-masing {puas_online:.1f}% (daring) "
        f"dan {puas_offline:.1f}% (non-daring), sedangkan ketidakpuasan hanya "
        f"berbeda sekitar {gap:.1f} poin persentase."
    )


def scholarship_insight(filtered_df: pd.DataFrame) -> str:
    recipient = filtered_df["scholarship"].eq("Yes")
    non_recipient = filtered_df["scholarship"].eq("No")
    puas_yes = category_share(filtered_df, recipient, "Puas")
    puas_no = category_share(filtered_df, non_recipient, "Puas")
    return (
        f"Mahasiswa nonpenerima beasiswa memiliki proporsi puas {puas_no:.1f}%, "
        f"dibandingkan {puas_yes:.1f}% pada penerima beasiswa. "
        "Selisih ini bersifat deskriptif dan belum membuktikan bahwa beasiswa "
        "memengaruhi kepuasan."
    )


def priority_insight(filtered_df: pd.DataFrame) -> str:
    field_stats = filtered_df.groupby("field_of_study", as_index=False).agg(
        pct_tidak_puas=(
            "satisfaction_category",
            lambda s: (s == "Tidak Puas").mean() * 100,
        ),
        avg_teaching=("teaching_quality_rating", "mean"),
        n=("student_id", "count"),
    )
    uni_avg_teaching = filtered_df["teaching_quality_rating"].mean()
    priority = field_stats[
        (field_stats["pct_tidak_puas"] >= field_stats["pct_tidak_puas"].median())
        & (field_stats["avg_teaching"] < uni_avg_teaching)
    ].sort_values("pct_tidak_puas", ascending=False)

    if priority.empty:
        top = field_stats.sort_values("pct_tidak_puas", ascending=False).iloc[0]
        return (
            f"Dalam data simulasi ini, **{top['field_of_study']}** "
            f"(n={int(top['n'])}) menunjukkan indikasi awal proporsi ketidakpuasan "
            f"tertinggi ({top['pct_tidak_puas']:.1f}%). "
            "Temuan bersifat deskriptif dan perlu dievaluasi lebih lanjut."
        )

    names = ", ".join(priority["field_of_study"].head(3).tolist())
    return (
        f"Dalam data simulasi ini, **{names}** menunjukkan indikasi awal sebagai "
        "bidang studi yang perlu dievaluasi lebih lanjut karena memiliki proporsi "
        "mahasiswa tidak puas relatif tinggi dan nilai kualitas pengajaran di bawah "
        "rata-rata keseluruhan. Kata “indikasi awal” penting karena belum ada "
        "pengujian statistik dan datanya bersifat sintetis."
    )


def country_dissatisfaction_map(filtered_df: pd.DataFrame):
    country_stats = filtered_df.groupby("country", as_index=False).agg(
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
    country_stats = country_stats.assign(
        iso_alpha=country_stats["country"].map(COUNTRY_ISO3)
    ).dropna(subset=["iso_alpha"])

    fig = px.choropleth(
        country_stats,
        locations="iso_alpha",
        color="pct_tidak_puas",
        hover_name="country",
        custom_data=["jumlah", "pct_tidak_puas", "pct_puas"],
        color_continuous_scale="OrRd",
        range_color=[0, 100],
        labels={"pct_tidak_puas": "% Tidak Puas"},
    )
    fig.update_traces(
        hovertemplate=(
            "Negara: %{hovertext}<br>"
            "Tidak puas: %{customdata[1]:.1f}%<br>"
            "Puas: %{customdata[2]:.1f}%<br>"
            "Jumlah responden: %{customdata[0]}<extra></extra>"
        )
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
        ),
        coloraxis_colorbar=dict(
            title="% Tidak Puas",
            ticksuffix="%",
        ),
    )
    return fig, country_stats


def country_dissatisfaction_bar(country_stats: pd.DataFrame):
    ordered = country_stats.sort_values("pct_tidak_puas", ascending=True)
    fig = px.bar(
        ordered,
        x="pct_tidak_puas",
        y="country",
        orientation="h",
        text=ordered.apply(
            lambda r: f"{r['pct_tidak_puas']:.1f}% (n={int(r['jumlah'])})",
            axis=1,
        ),
        labels={
            "pct_tidak_puas": "Proporsi Tidak Puas (%)",
            "country": "Negara Asal",
        },
        color="pct_tidak_puas",
        color_continuous_scale="OrRd",
        range_color=[0, 100],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=40, t=20, b=20),
        xaxis=dict(range=[0, 100]),
        coloraxis_showscale=False,
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
        st.subheader("Distribusi tingkat kepuasan responden")
        st.caption(
            "Grafik menunjukkan distribusi seluruh tingkat kepuasan, sehingga rektorat "
            "tidak hanya bergantung pada satu nilai rata-rata."
        )
        st.plotly_chart(
            satisfaction_distribution_chart(filtered_df),
            use_container_width=True,
        )
    with col_map:
        st.subheader("Proporsi mahasiswa tidak puas menurut negara asal")
        st.caption(
            "Warna peta memakai skala tetap 0–100% agar perbedaan antarnegara "
            "tidak terlihat lebih dramatis dari angka sebenarnya. "
            "Ini bukan lokasi kampus, melainkan asal responden."
        )
        map_fig, country_stats = country_dissatisfaction_map(filtered_df)
        st.plotly_chart(map_fig, use_container_width=True)
        small_n = country_stats[country_stats["jumlah"] < MIN_SAMPLE_WARNING]
        if not small_n.empty:
            names = ", ".join(small_n["country"].tolist())
            st.warning(
                f"Kelompok dengan kurang dari {MIN_SAMPLE_WARNING} responden "
                f"perlu diinterpretasikan secara hati-hati: {names}."
            )

    with st.expander("Peringkat negara (bar chart — lebih akurat untuk negara kecil)"):
        st.plotly_chart(
            country_dissatisfaction_bar(country_stats),
            use_container_width=True,
        )

    st.divider()
    st.header("2. Kelompok yang Memerlukan Perhatian")
    st.subheader("Distribusi kepuasan menurut bidang studi")
    st.caption(
        "Diurutkan berdasarkan proporsi mahasiswa tidak puas tertinggi. "
        "Proporsi digunakan agar perbandingan antarbidang tetap adil meskipun "
        "jumlah responden berbeda. Persentase pada bagian merah menunjukkan "
        "proporsi Tidak Puas."
    )
    st.plotly_chart(field_satisfaction_chart(filtered_df), use_container_width=True)

    st.subheader("Kualitas pengajaran dan fasilitas per bidang studi")
    st.caption(
        "Skala sumbu tetap 1–5 agar perbedaan tidak dilebih-lebihkan. "
        "Garis referensi menunjukkan rata-rata universitas. "
        "Selisih antarkelompok pada data ini relatif kecil."
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
            "Setiap baris berjumlah 100%: dari mahasiswa dengan rating pengajaran "
            "tertentu, berapa persen yang puas, netral, dan tidak puas?"
        )
        st.plotly_chart(
            rating_satisfaction_heatmap(
                filtered_df,
                "teaching_quality_rating",
                "Kualitas Pengajaran vs Kepuasan (%)",
            ),
            use_container_width=True,
        )
    with right:
        st.subheader("Fasilitas kampus vs kepuasan")
        st.caption(
            "Setiap baris berjumlah 100%: dari mahasiswa dengan rating fasilitas "
            "tertentu, berapa persen yang puas, netral, dan tidak puas?"
        )
        st.plotly_chart(
            rating_satisfaction_heatmap(
                filtered_df,
                "campus_facilities_rating",
                "Fasilitas Kampus vs Kepuasan (%)",
            ),
            use_container_width=True,
        )
    st.info(
        "Pada data simulasi ini, peningkatan rating pengajaran maupun fasilitas "
        "belum menunjukkan pergeseran tingkat kepuasan yang konsisten. "
        "Temuan bersifat deskriptif dan tidak menunjukkan hubungan sebab-akibat."
    )

    st.divider()
    st.header("4. Perbandingan Pengalaman Mahasiswa")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Kelas daring vs non-daring")
        st.plotly_chart(
            stacked_group_chart(
                filtered_df,
                "online_classes",
                {"Yes": "Daring", "No": "Non-daring"},
            ),
            use_container_width=True,
        )
        st.info(online_classes_insight(filtered_df))
    with col_b:
        st.subheader("Penerima vs nonpenerima beasiswa")
        st.plotly_chart(
            stacked_group_chart(
                filtered_df,
                "scholarship",
                {"Yes": "Penerima", "No": "Nonpenerima"},
            ),
            use_container_width=True,
        )
        st.info(scholarship_insight(filtered_df))

    st.divider()
    st.header("5. Data Detail dan Catatan")
    detail_view = (
        filtered_df[DISPLAY_COLUMNS]
        .sort_values(["field_of_study", "program_level", "student_id"])
        .rename(columns=DISPLAY_COLUMN_LABELS)
    )
    st.dataframe(detail_view, use_container_width=True, hide_index=True)

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
