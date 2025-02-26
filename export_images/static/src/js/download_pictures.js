/** @odoo-module **/
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";
import { _lt } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

const action_registry = registry.category("actions");

async function getZipFileBlob(partners) {
  const zipWriter = new zip.ZipWriter(new zip.BlobWriter("application/zip"));
  await Promise.all(
    partners.map(async (partner) => {
      let id = partner[0];
      let name = partner[1].replace(/\s+/g, "_");
      const url = `/web/image/res.partner/${id}/image_1920/288x320`;
      zipWriter.add(`${id}_${name}.jpg`, new zip.HttpReader(url));
    })
  );
  return zipWriter.close();
}

function downloadFile(blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  Object.assign(a, {
    download: "contact_pictures.zip",
    href: url,
  });
  a.click();
  // remove the blob url after the download
  // to avoid memory leaks
  URL.revokeObjectURL(url);
  a.remove();
}
async function actionDownloadPictures(parent, { params }) {
  // Lazy loading the zip library, we don't want it to be loaded at all
  // times
  await loadBundle("export_images.external_libraries");
  // check if zip library is available
  if (!window.zip) {
    parent.services?.dialog.add(AlertDialog, {
      title: "Error",
      body: "Error with zip.js library. Please contact support.",
    });
    return;
  }
  const partners = params.partner_ids;
  await getZipFileBlob(partners).then(downloadFile);
}
action_registry.add("action_download_contact_pictures", actionDownloadPictures);

return actionDownloadPictures;
