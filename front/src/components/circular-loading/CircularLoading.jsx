import './../../assets/css/circular-loading.css';

const CircularLoading = () => {
    return (
        <div className="circular-loading-root">
            <span className="circular-loading-progressbar">
                <svg className="circular-loading-svg" viewBox="22 22 44 44">
                    <circle className="circular-loading-circle" cx="44" cy="44" r="20.2" fill="none" strokeWidth="3.6">
                    </circle>
                </svg>
            </span>
        </div>
    );
}

export default CircularLoading;