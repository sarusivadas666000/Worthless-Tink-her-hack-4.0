async function generateVideo() {
  const start = document.getElementById("startImage").files[0];
  const end = document.getElementById("endImage").files[0];

  if (!start || !end) {
    alert("Upload both images");
    return;
  }

  const formData = new FormData();
  formData.append("initial_image", start);
  formData.append("final_image", end);

  document.getElementById("loader").classList.remove("hidden");

  const response = await fetch("http://localhost:8000/generate-video", {
    method: "POST",
    body: formData,
  });

  const blob = await response.blob();
  const videoURL = URL.createObjectURL(blob);

  const video = document.getElementById("video");
  video.src = videoURL;
  video.classList.remove("hidden");

  document.getElementById("loader").classList.add("hidden");
}
